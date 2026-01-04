import httpx

from abc import ABC, abstractmethod
from typing import Any, Dict, List

class CampaignService(ABC):
    
    @abstractmethod
    def get_campaigns(self) -> List[str]:
        raise NotImplementedError
    
    @abstractmethod
    def get_campaign_details(self, campaign_name: str) -> Dict[str, Any]:
        raise NotImplementedError
    
    async def get_campaign_details_async(
        self,
        client: httpx.AsyncClient,
        campaign_name: str
    ) -> Dict[str, Any]:
        raise NotImplementedError