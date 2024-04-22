from sqlalchemy import select, func
from dateutil.parser import parse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from nest.core.decorators import async_db_request_handler

from src.facebook.facebook_entity import FacebookAdsCustomers


class FacebookAdsService:
    @async_db_request_handler
    async def get_entities_by_filters(
        self, filters: Dict[str, Any], page: int, per_page: int, session: AsyncSession
    ) -> List[FacebookAdsCustomers]:
        """
        Fetches Facebook customer entities based on provided filters, pagination, and error handling.

        Args:
            filters: Dictionary containing filter criteria (field names and values).
            page: Page number for pagination (starts from 1).
            per_page: Number of entities per page for pagination.
            session: AsyncSession object for database interaction.

        Returns:
            List[FacebookAdsCustomers]: List of fetched Facebook customer entities.
            int: Total count of entities matching the filters.
            Exception: Any exception encountered during data retrieval.
        """

        try:
            # Construct the main query with filtering logic
            query = select(FacebookAdsCustomers)
            if filters:
                conditions = []
                for field, value in filters.items():
                    # Handle potential date parsing
                    if isinstance(value, str) and field in ["date_start", "date_end", "inserted_at"]:
                        try:
                            value = parse(value)
                        except ValueError:
                            pass
                    conditions.append(getattr(FacebookAdsCustomers, field) == value)
                query = query.where(*conditions)

            # Apply pagination with appropriate offset calculation
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page)

            # Execute the query to fetch entities
            result = await session.execute(query)
            entities: List[FacebookAdsCustomers] = result.scalars().all()

            # Construct and execute the count query
            count_query = select(func.count()).select_from(FacebookAdsCustomers)
            if filters:
                count_query = count_query.where(*conditions)
            count_result = await session.execute(count_query)
            total_count = count_result.scalar()

            return entities, total_count, None

        except Exception as error:
            return [], 0, error