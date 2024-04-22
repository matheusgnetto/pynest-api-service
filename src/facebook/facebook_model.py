from pydantic import BaseModel, Field, validator
from typing import Optional

class FacebookAdsFilter(BaseModel):
    unit_id: str
    project_id: Optional[str] = None
    customer_new_id: Optional[str] = None
    campaign_id: Optional[str] = None
    adset_id: Optional[str] = None
    ad_id: Optional[str] = None
    date_start: Optional[str] = None
    date_stop: Optional[str] = None
    account: Optional[str] = None

    @validator("date_start")
    def validate_date_start_format(cls, value, values):
        if "date_stop" in values and not value:
            return value
        if value:
            from dateutil.parser import parse
            try:
                parsed_date = parse(value)
                if parsed_date.strftime("%Y-%m-%d") != value:
                    raise ValueError(f"Invalid date format: {value} (ISO 8601 expected)")
                return value
            except ValueError:
                raise ValueError(f"Invalid date format: {value}")
        return value

    @validator("date_stop")
    def validate_date_stop_format(cls, value, values):
        if "date_start" in values and not value:
            return value
        if value:
            from dateutil.parser import parse
            try:
                parsed_date = parse(value)
                if parsed_date.strftime("%Y-%m-%d") != value:
                    raise ValueError(f"Invalid date format: {value} (ISO 8601 expected)")
                return value
            except ValueError:
                raise ValueError(f"Invalid date format: {value}")
        return value