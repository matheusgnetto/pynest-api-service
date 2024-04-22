from .facebook_service import FacebookAdsService
from .facebook_controller import FacebookAdsController


class FacebookModule:

    def __init__(self):
        self.providers = [FacebookAdsService]
        self.controllers = [FacebookAdsController]
