from services.factory import CampaignServiceFactory

service = CampaignServiceFactory.get_service("unitec", "digital")

campaigns = service.get_campaigns()

print("Total campañas:", len(campaigns))
print("Primeras 5:", campaigns[:5])

raw = service.get_campaign_details(campaigns[0])