import asyncio
import httpx

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from services.factory import CampaignServiceFactory
from exporters.normalizer import normalize_campaign_details
from exporters.excel_exporter import ExcelExporter
from schemas.campaign import CampaignDetailsResponse, CampaignDetails

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("/export")
async def export_campaigns(
    request: Request,
    brand: str,
    channel: str
):
    try:
        service = CampaignServiceFactory.get_service(brand, channel)
        campaign_names = service.get_campaigns()

        semaphore = asyncio.Semaphore(5)

        async def fetch_campaign(client, name):
            if await request.is_disconnected():
                raise asyncio.CancelledError("Client disconnected")
            async with semaphore:
                return name, await service.get_campaign_details_async(client, name)

        async with httpx.AsyncClient(timeout=httpx.Timeout(120)) as client:
            tasks = [fetch_campaign(client, name) for name in campaign_names]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        all_rows = []

        for result in results:
            if isinstance(result, asyncio.CancelledError):
                # cliente cerró pestaña → abortar limpio
                raise HTTPException(status_code=499, detail="Client disconnected")

            if isinstance(result, BaseException):
                print(f"⚠️ Campaña fallida: {result}")
                continue

            campaign_name, raw = result
            if not raw:
                continue

            response = CampaignDetailsResponse(
                brand=brand,
                campaign_name=campaign_name,
                channels={
                    channel: CampaignDetails(
                        members=raw.get("Members"),
                        attention_levels=raw.get("AttentionLevels"),
                        thresholds=raw.get("Thresholds"),
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

    except asyncio.CancelledError:
        # 🔑 evita 500
        raise HTTPException(status_code=499, detail="Request cancelled")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
