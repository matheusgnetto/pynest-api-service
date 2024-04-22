from http.client import HTTPException
from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .facebook_model import FacebookAdsCustomersData
from .facebook_service import FacebookAdsService
from typing import Dict, Any
from config import config
from fastapi import Request


@Controller("facebook")
class FacebookAdsController:
    service: FacebookAdsService = Depends(FacebookAdsService)
    session: AsyncSession = Depends(config.get_db)

    @Get("/")
    async def get_facebook_customers(
        self,
        request: Request,
        filter_data: FacebookAdsCustomersData,
        page: int = 1,
        per_page: int = 10,
        async_session: AsyncSession = Depends(config.get_db)
    ) -> Dict[str, Any]:
        """
        Fetches all Facebook customer data based on provided filters.

        Args:
            request: Request object containing query parameters.
            filter_data: Validated filter data from Pydantic model.
            page (int, optional): Pagination page number. Defaults to 1.
            per_page (int, optional): Items per page. Defaults to 10.

        Returns:
            Dict[str, Any]: Response containing success status, data, and record count.
        """

        try:
            # Retrieve filter data from request query parameters
            filter_data = FacebookAdsCustomersData(**request.query_params)

            # Pydantic parsing already ensured valid data in filter_data
            entities, total_count, error = await self.service.get_entities_by_filters(
                filter_data.dict(), page, per_page, async_session
            )

            if total_count == 0:
                raise Exception("No data found based on the provided filters")

            total_pages = (total_count + per_page - 1) // per_page

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