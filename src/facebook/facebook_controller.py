from datetime import datetime
from http.client import HTTPException
from fastapi import Query
from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .facebook_model import FacebookAdsFilter
from .facebook_service import FacebookAdsService, validate_date_range
from typing import Dict, Any, Optional
from config import config

@Controller("facebook")
class FacebookAdsController:
    service: FacebookAdsService = Depends(FacebookAdsService)
    session: AsyncSession = Depends(config.get_db)

    @Get("/")
    async def get_facebook_customers(
        self,
        unit_id: str = Query(..., description="Unit ID"),
        project_id: Optional[str] = Query(None, description="Project ID in Mediahub"),
        customer_new_id: Optional[str] = Query(None, description="Customer ID in Mediahub"),
        campaign_id: Optional[str] = Query(None, description="Campaign ID in Facebook Account"),
        adset_id: Optional[str] = Query(None, description="Adset ID in Facebook Account"),
        ad_id: Optional[str] = Query(None, description="AD ID in Facebook Account"),
        date_start: Optional[str] = Query(None, description="Campaign date start (YYYY-MM-DD)"),
        date_stop: Optional[str] = Query(None, description="Campaign date end (YYYY-MM-DD)"),
        account: Optional[str] = Query(None, description="Facebook Account ID"),
        page: int = Query(1, ge=1, description="Pagination page number"),
        per_page: int = Query(500, ge=1, le=1000, description="Items per page")
    ) -> Dict[str, Any]:
        """
        `Fetches all Facebook customer data based on provided filters.`

        **Params:**
        - **unit_id** `(str):` Unit ID in Mediahub
        - **project_id** `(str, optional):` Project ID in Mediahub
        - **customer_new_id** `(str, optional):` Customer ID in Mediahub
        - **campaign_id** `(str, optional):` Campaign ID in Facebook Account
        - **adset_id** `(str, optional):` Adset ID in Facebook Account
        - **ad_id** `(str, optional):` AD ID in Facebook Account
        - **date_start** `(str, optional):` Campaign date start (YYYY-MM-DD)
        - **date_stop** `(str, optional):` Campaign date end (YYYY-MM-DD)
        - **account** `(str, optional):` Facebook Account ID
        - **page** `(int, optional):` Pagination page number (default is 1)
        - **per_page** `(int, optional):` Items per page (default is 500, max is 1000)

        **Returns:**
        - `Dict[str, Any]:` Response containing success status, data, and record count.

        """
        try:
            
            filters = FacebookAdsFilter(
                unit_id=unit_id,
                project_id=project_id,
                customer_new_id=customer_new_id,
                campaign_id=campaign_id,
                adset_id=adset_id,
                ad_id=ad_id,
                date_start=date_start,
                date_stop=date_stop,
                account=account
            )
            print(filters)

            entities, total_count, error = await self.service.get_entities_by_filters(
                filters.dict(exclude_unset=True),
                page, per_page, self.session
            )

            if total_count == 0:
                raise Exception("No data found based on the provided filters")

            total_pages = (total_count + per_page - 1) // per_page
            if per_page > 1000:
                per_page = 1000

            payload = {
                "success": True,
                "data": entities,
                "records": total_count,
                "current_page": page,
                "per_page": per_page,
                "total_pages": total_pages,
            }

        except Exception as error:
            payload = {
                "success": False,
                "errors": [str(error)],
            }

        return payload