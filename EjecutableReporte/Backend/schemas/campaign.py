from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class CampaignListResponse(BaseModel):
    channel: str
    campaigns: List[str]
    
class CampaignDetails(BaseModel):
    members: Optional[Dict[str, Any]] = Field(default_factory=dict)
    attention_levels: Optional[Any] = Field(default_factory=dict)
    thresholds: Optional[Any] = Field(default_factory=dict)

class CampaignDetailsByChannel(BaseModel):
    channel: str
    data: CampaignDetails
    
class CampaignDetailsResponse(BaseModel):
    brand: str
    campaign_name: str
    channels: Dict[str, CampaignDetails]