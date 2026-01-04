import requests
import httpx

from typing import Any, Dict, List
from services.base import CampaignService

class HttpCampaignService(CampaignService):
    def __init__(self, url: str, token: str):
        if not url or not token:
            raise RuntimeError("API_URL o API_TOKEN no configurados")
        
        self.url = url
        self.token = token
        
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "identity",
        }
        
    def get_campaigns(self) -> List[str]:
        payload = {
            "limit": 1000,
            "numberPage": 1,
            "query": {"Name": "", "Description": ""},
            "columns": ["Name"],
        }
        
        response = requests.post(self.url, headers=self._headers(), json=payload)
        
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            return {}
        
        data = response.json()
        return [row["Name"] for row in data.get("rows", [])]
    
    async def get_campaign_details_async(
        self, 
        client: httpx.AsyncClient,
        campaign_name: str
        ) -> Dict[str, Any]:
        payload = {
            "query": {"Name": campaign_name},
            "columns": ["Members", "AttentionLevels", "Thresholds"],
        }
        
        response = await client.post(
            self.url, 
            headers=self._headers(), 
            json=payload
        )
        
        if response.status_code != 200:
            response.raise_for_status()
            
        data = response.json()
        if not data.get("rows"):
            return {}
        
        return data["rows"][0]
    
    def get_campaign_details(self, campaign_name: str) -> Dict[str, Any]:
        payload = {
            "query": {"Name": campaign_name},
            "columns": ["Members", "AttentionLevels", "Thresholds"],
        }

        response = requests.post(
            self.url,
            headers=self._headers(),
            json=payload
        )
        response.raise_for_status()

        data = response.json()
        if not data.get("rows"):
            return {}

        return data["rows"][0]
