import datetime
from config import config
from sqlalchemy import Table, MetaData
from sqlalchemy import Column, Integer, String, Float, DateTime

metadata = MetaData()
    
class FacebookAdsCustomers(config.Base):
    __tablename__ = "facebook_ads_customers"
    metadata = metadata

    id_insert = Column(String, primary_key=True)
    campaign_name = Column(String)
    campaign_id = Column(String)
    adset_name = Column(String)
    adset_id = Column(String)
    ad_name = Column(String)
    ad_id = Column(String)
    clicks = Column(Integer)
    link_clicks = Column(Integer)
    reach = Column(Integer)
    impressions = Column(Integer)
    objective = Column(String)
    spend = Column(Float)
    video_view = Column(Integer)
    post_engagement = Column(Integer)
    add_to_cart = Column(Integer)
    purchase = Column(Integer)
    purchase_values = Column(Float)
    custom = Column(String)
    lead = Column(String)
    initiated_checkout = Column(Integer)
    date_start = Column(String)
    date_stop = Column(String)
    account = Column(String)
    customer_id = Column(String)
    unit_id = Column(String)
    year_month = Column(String)
    project_id = Column(String)
    customer_new_id = Column(String)
    inserted_at = Column(DateTime, default=datetime.datetime.utcnow)

