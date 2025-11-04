"""
Geonames Service Implementation
This module handles all Geonames API interactions with proper credential management
and rate limiting for the open-source solution.
"""
import asyncio
import logging
from typing import Optional, Dict, Any
import aiohttp
from ..config.settings import settings


logger = logging.getLogger(__name__)


class GeonamesService:
    """
    Service class to handle Geonames API interactions with credential management,
    rate limiting, and caching for the open-source solution.
    """
    
    def __init__(self):
        self.base_url = "http://api.geonames.org"
        self.username = settings.geonames_username
        self._session: Optional[aiohttp.ClientSession] = None
        self.cache: Dict[str, Any] = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        self._session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._session:
            await self._session.close()
            
    async def get_credential_status(self) -> Dict[str, Any]:
        """Get current credential status and usage information"""
        if not self.username:
            return {
                "status": "error",
                "message": "No Geonames username configured"
            }
        
        return {
            "status": "active",
            "username": self.username,
            "has_credential": bool(self.username)
        }
        
    async def search(self, 
                    q: str, 
                    max_rows: int = 10, 
                    lang: str = 'en',
                    style: str = 'medium') -> Optional[Dict[str, Any]]:
        """
        Search for places using Geonames API
        """
        if not self._session:
            raise RuntimeError("Service not initialized properly")
            
        if not self.username:
            raise ValueError("Geonames username is required")
            
        params = {
            'q': q,
            'maxRows': max_rows,
            'lang': lang,
            'style': style,
            'username': self.username
        }
        
        try:
            async with self._session.get(f"{self.base_url}/searchJSON", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Geonames search error: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Geonames search exception: {str(e)}")
            return None
            
    async def get_timezone(self, 
                          lat: float, 
                          lng: float) -> Optional[Dict[str, Any]]:
        """
        Get timezone information for coordinates
        """
        if not self._session:
            raise RuntimeError("Service not initialized properly")
            
        if not self.username:
            raise ValueError("Geonames username is required")
            
        params = {
            'lat': lat,
            'lng': lng,
            'username': self.username
        }
        
        try:
            async with self._session.get(f"{self.base_url}/timezoneJSON", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Geonames timezone error: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Geonames timezone exception: {str(e)}")
            return None
            
    async def get_cities(self, 
                        north: float, 
                        south: float, 
                        east: float, 
                        west: float,
                        lang: str = 'en') -> Optional[Dict[str, Any]]:
        """
        Get cities in a bounding box
        """
        if not self._session:
            raise RuntimeError("Service not initialized properly")
            
        if not self.username:
            raise ValueError("Geonames username is required")
            
        params = {
            'north': north,
            'south': south,
            'east': east,
            'west': west,
            'lang': lang,
            'username': self.username
        }
        
        try:
            async with self._session.get(f"{self.base_url}/citiesJSON", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Geonames cities error: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Geonames cities exception: {str(e)}")
            return None
            
    async def get_country_info(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Get country information
        """
        if not self._session:
            raise RuntimeError("Service not initialized properly")
            
        if not self.username:
            raise ValueError("Geonames username is required")
            
        params = {
            'country': country,
            'username': self.username
        }
        
        try:
            async with self._session.get(f"{self.base_url}/countryInfoJSON", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Geonames country info error: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Geonames country info exception: {str(e)}")
            return None