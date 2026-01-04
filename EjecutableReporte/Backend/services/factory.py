from typing import Dict

from services.base import CampaignService

#UNITEC
from services.unitec.digital_service import DigitalCampaignService as UnitecDigital
from services.unitec.dialer_service import DialerCampaignService as UnitecDialer

#UVM
from services.uvm.digital_service import DigitalCampaignService as UvmDigital
from services.uvm.dialer_service import DialerCampaignService as UvmDialer


class CampaignServiceFactory:
    
    """
    Factory para resolver servicios de campañas por marca y canal.
    """
    
    @staticmethod
    def get_service(brand: str, channel: str) -> CampaignService:
        brand = brand.lower()
        channel = channel.lower()
        
        if brand == "unitec":
            if channel == "digital":
                return UnitecDigital()
            if channel == "dialer":
                return UnitecDialer()
        
        if brand == "uvm":
            if channel == "digital":
                return UvmDigital()
            if channel == "dialer":
                return UvmDialer()
            
        raise ValueError(f"Servicio no soportadoL: brand={brand}, channel={channel}")
    
    @staticmethod
    def get_all_services(brand: str) -> Dict[str, CampaignService]:
        """
        Obtener TODOS los servicios de una marca.
        """
        brand = brand.lower()
        
        if brand == "unitec":
            return {
                "digital": UnitecDigital(),
                "dialer": UnitecDialer(),
            }
            
        if brand == "uvm":
            return {
                "digital": UvmDigital(),
                "dialer": UvmDialer(),
            }
            
        raise ValueError(f"Marca no soportada: {brand}")