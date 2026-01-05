import asyncio
import httpx

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from services.factory import CampaignServiceFactory
from exporters.normalizer import normalize_campaign_details
from exporters.excel_exporter import ExcelExporter
from schemas.campaign import CampaignDetailsResponse, CampaignDetails

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("/export")
async def export_campaigns(
    brand: str,
    channel: str
):
    try:
        service = CampaignServiceFactory.get_service(brand, channel)
        campaign_names = service.get_campaigns()
        
        semaphore = asyncio.Semaphore(5) #Controla concurrencia
        
        async def fetch_campaign(client, name):
            async with semaphore:
                return name, await service.get_campaign_details_async(client, name)
        
        timeout = httpx.Timeout(
            connect=10.0,
            read=120.0,
            write=10.0,
            pool=10.0
        )    
        async with httpx.AsyncClient(timeout=timeout) as client:
            tasks = [
                fetch_campaign(client, name)
                for name in campaign_names
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        all_rows = []
        
        for result in results:
            if isinstance(result, BaseException):
                print(f"⚠️ Campaña fallida: {result}")
                continue
            
            campaign_name, raw = result
            
            if not raw:
                continue
            
            print("RAW RESPONSE:", raw)
            
            response = CampaignDetailsResponse(
                brand=brand,
                campaign_name=campaign_name,
                channels={
                    channel: CampaignDetails(
                        members=raw.get("Members"),
                        attention_levels=raw.get("AttentionLevels"),
                        thresholds=raw.get('Thresholds'),
                    )
                }
            )
            
            all_rows.extend(normalize_campaign_details(response))
        excel = ExcelExporter.export(all_rows)
        
        return StreamingResponse(
            excel,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="{brand}_{channel}.xlsx"'
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))