from services.http_base import HttpCampaignService
from config.settings import DIALER_UVM_API_URL, DIALER_UVM_API_TOKEN

class DialerCampaignService(HttpCampaignService):
    def __init__(self):
        if not DIALER_UVM_API_URL or not DIALER_UVM_API_TOKEN:
            raise RuntimeError("DIALER_API_URL o DIALER_API_TOKEN no configurados")
        
        super().__init__(
            url=DIALER_UVM_API_URL,
            token=DIALER_UVM_API_TOKEN
        )