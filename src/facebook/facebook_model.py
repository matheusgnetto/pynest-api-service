from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class FacebookAdsCustomersData(BaseModel):
    """
    Represents Facebook Ads customer data with data type validation and constraints.
    """

    # Database ID (if applicable)
    id_insert: Optional[str] = Field(alias="id")  # Use a clearer alias

    # Campaign information
    campaign_name: Optional[str] = Field(max_length=255)
    campaign_id: Optional[str] = Field(max_length=255)

    # Adset information
    adset_name: Optional[str] = Field(max_length=255)
    adset_id: Optional[str] = Field(max_length=255)

    # Ad information
    ad_name: Optional[str] = Field(max_length=255)
    ad_id: Optional[str] = Field(max_length=255)

    # Performance metrics
    clicks: Optional[int] = Field(ge=0)  # Ensure non-negative values
    link_clicks: Optional[int] = Field(ge=0)
    reach: Optional[int] = Field(ge=0)
    impressions: Optional[int] = Field(ge=0)

    # Campaign objective
    objective: Optional[str] = Field(max_length=255)

    # Cost metrics
    spend: Optional[float] = Field(ge=0.0)  # Ensure non-negative values

    # Engagement metrics
    video_view: Optional[int] = Field(ge=0)
    post_engagement: Optional[int] = Field(ge=0)

    # Conversion metrics
    add_to_cart: Optional[int] = Field(ge=0)
    purchase: Optional[int] = Field(ge=0)
    purchase_values: Optional[float] = Field(ge=0.0)

    # Custom data
    custom: Optional[str]

    # Lead data
    lead: Optional[str]

    # Other metrics
    initiated_checkout: Optional[int] = Field(ge=0)

    # Date information
    date_start: Optional[str] = Field(format="%Y-%m-%d")

    # Account and customer association
    account: Optional[str] = Field(max_length=255)
    customer_id: Optional[str] = Field(max_length=255)
    unit_id: Optional[str] = Field(max_length=255)

    # Project and customer ID (potentially for filtering)
    project_id: Optional[str] = Field(max_length=255)
    customer_new_id: Optional[str] = Field(max_length=255)

    # Data insertion timestamp
    inserted_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("date_start")
    def validate_date_format(cls, value):
        """
        Validates the date format using dateutil.
        """
        from dateutil.parser import parse
        try:
            parse(value)
            return value
        except ValueError:
            raise ValueError(f"Invalid date format: {value}")