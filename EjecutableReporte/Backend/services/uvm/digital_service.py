from services.http_base import HttpCampaignService
from config.settings import DIGITAL_UVM_API_URL, DIGITAL_UVM_API_TOKEN

class DigitalCampaignService(HttpCampaignService):
    
    def __init__(self):
        if not DIGITAL_UVM_API_URL or not DIGITAL_UVM_API_TOKEN:
            raise RuntimeError("DIGITAL_API_URL o DIGITAL_API_TOKEN no configurados")
        
        super().__init__(
            url=DIGITAL_UVM_API_URL,
            token=DIGITAL_UVM_API_TOKEN
        )