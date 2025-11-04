"""
PT-BR Localization and Optimization Module
Provides Portuguese/Brazilian specific optimizations for the Geonames service
"""
import logging
from typing import Dict, List, Optional, Any
from .service import GeonamesService


logger = logging.getLogger(__name__)


class PtBrOptimizer:
    """
    Provides Brazilian/Portuguese specific optimizations and localization
    for Geonames services in the open-source solution.
    """
    
    # Common Brazilian cities with Portuguese names
    BRAZILIAN_CITIES = {
        "são paulo": "São Paulo",
        "rio de janeiro": "Rio de Janeiro", 
        "brasília": "Brasília",
        "salvador": "Salvador",
        "fortaleza": "Fortaleza",
        "belo horizonte": "Belo Horizonte",
        "manaus": "Manaus",
        "curitiba": "Curitiba",
        "recife": "Recife",
        "porto alegre": "Porto Alegre",
        "belém": "Belém",
        "goiânia": "Goiânia",
        "guarulhos": "Guarulhos",
        "campinas": "Campinas",
        "sobral": "Sobral",
        "santos": "Santos"
    }
    
    # Brazilian state capitals with Portuguese names
    BRAZIL_STATE_CAPITALS = {
        "acre": "Rio Branco",
        "alagoas": "Maceió",
        "amapá": "Macapá",
        "amazonas": "Manaus",
        "bahia": "Salvador",
        "ceará": "Fortaleza",
        "distrito federal": "Brasília",
        "espírito santo": "Vitória",
        "goiás": "Goiânia",
        "maranhão": "São Luís",
        "mato grosso": "Cuiabá",
        "mato grosso do sul": "Campo Grande",
        "minas gerais": "Belo Horizonte",
        "pará": "Belém",
        "paraíba": "João Pessoa",
        "paraná": "Curitiba",
        "pernambuco": "Recife",
        "piauí": "Teresina",
        "rio de janeiro": "Rio de Janeiro",
        "rio grande do norte": "Natal",
        "rio grande do sul": "Porto Alegre",
        "rondônia": "Porto Velho",
        "roraima": "Boa Vista",
        "santa catarina": "Florianópolis",
        "são paulo": "São Paulo",
        "sergipe": "Aracaju",
        "tocantins": "Palmas"
    }
    
    def __init__(self, geonames_service: GeonamesService):
        self.geonames_service = geonames_service
        
    def get_portuguese_city_name(self, city_name: str) -> str:
        """Get the Portuguese name for a city if available"""
        normalized = city_name.lower()
        return self.BRAZILIAN_CITIES.get(normalized, city_name)
        
    def get_brazilian_state_capital(self, state: str) -> Optional[str]:
        """Get the capital of a Brazilian state"""
        normalized = state.lower()
        return self.BRAZIL_STATE_CAPITALS.get(normalized)
        
    async def search_brazilian_places(self, 
                                     query: str, 
                                     max_results: int = 10) -> Optional[Dict[str, Any]]:
        """Optimized search for Brazilian places with Portuguese names"""
        # First try to search with the original query
        result = await self.geonames_service.search(query, max_results, lang='pt')
        
        if result and result.get('geonames'):
            # Enhance results with Portuguese names where available
            for geoname in result['geonames']:
                if geoname.get('countryCode') == 'BR':
                    # Add Portuguese name if available
                    portuguese_name = self.get_portuguese_city_name(geoname.get('name', ''))
                    if portuguese_name != geoname.get('name'):
                        geoname['portugueseName'] = portuguese_name
                        
        return result
        
    async def get_brazil_timezone(self, city_name: str) -> Optional[str]:
        """Get the timezone for a Brazilian city"""
        # Map common Brazilian cities to their timezones
        brazil_timezones = {
            "são paulo": "America/Sao_Paulo",
            "rio de janeiro": "America/Sao_Paulo", 
            "brasília": "America/Sao_Paulo",
            "salvador": "America/Bahia",
            "fortaleza": "America/Fortaleza",
            "belo horizonte": "America/Sao_Paulo",
            "manaus": "America/Manaus",
            "curitiba": "America/Sao_Paulo",
            "recife": "America/Recife",
            "porto alegre": "America/Sao_Paulo",
            "belém": "America/Belem",
            "goiânia": "America/Sao_Paulo",
            "boavista": "America/Boa_Vista"
        }
        
        normalized = city_name.lower()
        return brazil_timezones.get(normalized)
        
    async def format_brazilian_location(self, 
                                       geoname: Dict[str, Any]) -> Dict[str, Any]:
        """Format location data with Brazilian-specific information"""
        formatted = {
            "name": geoname.get('name'),
            "portuguese_name": self.get_portuguese_city_name(geoname.get('name', '')),
            "country_code": geoname.get('countryCode'),
            "country_name": geoname.get('countryName'),
            "admin_code": geoname.get('adminCode1'),
            "admin_name": geoname.get('adminName1'),
            "latitude": geoname.get('lat'),
            "longitude": geoname.get('lng'),
            "population": geoname.get('population'),
            "timezone": await self.get_brazil_timezone(geoname.get('name', '')),
            "fcode": geoname.get('fcode')
        }
        
        # If it's a Brazilian location, add Brazilian-specific info
        if geoname.get('countryCode') == 'BR':
            formatted["is_brazilian"] = True
            formatted["timezone"] = formatted["timezone"] or "America/Sao_Paulo"
            
        return formatted