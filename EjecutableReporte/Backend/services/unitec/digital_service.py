from services.http_base import HttpCampaignService
from config.settings import DIGITAL_UNITEC_API_URL, DIGITAL_UNITEC_API_TOKEN

class DigitalCampaignService(HttpCampaignService):
    
    def __init__(self):
        
        if not DIGITAL_UNITEC_API_URL or not DIGITAL_UNITEC_API_TOKEN:
            raise RuntimeError("DIGITAL_UNITEC_API_URL o DIGITAL_UNITEC_API_TOKEN no configurados")
        
        super().__init__(
            url=DIGITAL_UNITEC_API_URL,
            token=DIGITAL_UNITEC_API_TOKEN
        )