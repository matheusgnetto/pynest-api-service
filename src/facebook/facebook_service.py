from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from nest.core.decorators import async_db_request_handler
from src.facebook.facebook_entity import FacebookAdsCustomers

def validate_date_range(date_start: Optional[str], date_stop: Optional[str]) -> None:
    """
    Validates the format of optional date_start and date_stop parameters.

    Args:
        date_start: Optional string representing the start date (YYYY-MM-DD).
        date_stop: Optional string representing the end date (YYYY-MM-DD).

    Raises:
        ValueError: If either date format is invalid or date_start is after date_stop.
    """
    if date_start and date_stop:
        try:
            parsed_start = datetime.strptime(date_start, "%Y-%m-%d")
            parsed_stop = datetime.strptime(date_stop, "%Y-%m-%d")
            if parsed_start > parsed_stop:
                raise ValueError("Start date cannot be after end date.")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")


class FacebookAdsService:
    @async_db_request_handler
    async def get_entities_by_filters(
        self,
        filters: Dict[str, Any],
        page: int,
        per_page: int,
        session: AsyncSession,
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
            date_start = filters.get("date_start")
            date_stop = filters.get("date_stop")

            # Validate date filters if provided
            validate_date_range(date_start, date_stop)

            conditions = []
            for field, value in filters.items():
                if field not in ["date_start", "date_stop"] and value is not None:
                    conditions.append(getattr(FacebookAdsCustomers, field) == value)

            # Apply filter conditions to the main query
            query = select(FacebookAdsCustomers)
            if conditions:
                query = query.where(*conditions)

            # Apply pagination with appropriate offset calculation
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page)

            # Execute the query to fetch entities
            result = await session.execute(query)
            entities: List[FacebookAdsCustomers] = result.scalars().all()

            # Construct and execute the count query
            count_query = select(func.count()).select_from(FacebookAdsCustomers)

            # Apply filter conditions to the count query
            if conditions:
                count_query = count_query.where(*conditions)

            count_result = await session.execute(count_query)
            total_count = count_result.scalar()

            return entities, total_count, None

        except Exception as error:
            return [], 0, error
