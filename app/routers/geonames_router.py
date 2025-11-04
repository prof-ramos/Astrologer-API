"""
Geonames API Router
Provides the API endpoints for Geonames functionality in the open-source solution
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional, Dict, Any
import logging
from ..geonames.service import GeonamesService
from ..geonames.credential_manager import CredentialManager
from ..geonames.rate_limiter import RateLimiter
from ..geonames.pt_br_optimizer import PtBrOptimizer
from ..utils.write_request_to_log import get_write_request_to_log
from ..config.settings import settings


logger = logging.getLogger(__name__)
write_request_to_log = get_write_request_to_log(logger)

router = APIRouter()

# Initialize services
geonames_service = GeonamesService()
credential_manager = CredentialManager()
rate_limiter = RateLimiter()
pt_br_optimizer = PtBrOptimizer(geonames_service)


@router.get("/api/v4/geonames/status", 
            response_description="Geonames service status",
            include_in_schema=True)
async def geonames_status(request: Request):
    """
    Get the status of the Geonames service including credential status and rate limiting.
    """
    write_request_to_log(20, request, "Geonames status check")
    
    try:
        # Check credential status
        credential_status = await credential_manager.validate_credential()
        
        # Check rate limiting status
        rate_limit_status = await rate_limiter.get_usage_stats()
        
        response = {
            "status": "OK",
            "service": "Geonames Open Source Service",
            "credential_status": credential_status,
            "rate_limiting": rate_limit_status,
            "timestamp": "datetime.now().isoformat()"  # In a real implementation
        }
        
        return response
    except Exception as e:
        logger.error(f"Geonames status error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/v4/geonames/search", 
            response_description="Search for places using Geonames",
            include_in_schema=True)
async def geonames_search(
    request: Request,
    q: str,
    max_rows: int = 10,
    lang: str = "en",
    style: str = "medium"
):
    """
    Search for places using Geonames API with built-in rate limiting and credential management.
    """
    write_request_to_log(20, request, f"Geonames search for: {q}")
    
    # Check rate limiting
    if not await rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            raise HTTPException(status_code=401, detail="Geonames credentials not configured")
            
        result = await geonames_service.search(q, max_rows, lang, style)
        
        if result is None:
            raise HTTPException(status_code=500, detail="Error contacting Geonames service")
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Geonames search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/v4/geonames/timezone", 
            response_description="Get timezone for coordinates",
            include_in_schema=True)
async def geonames_timezone(
    request: Request,
    lat: float,
    lng: float
):
    """
    Get timezone information for specific coordinates using Geonames API.
    """
    write_request_to_log(20, request, f"Geonames timezone for coordinates: {lat}, {lng}")
    
    # Check rate limiting
    if not await rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            raise HTTPException(status_code=401, detail="Geonames credentials not configured")
            
        result = await geonames_service.get_timezone(lat, lng)
        
        if result is None:
            raise HTTPException(status_code=500, detail="Error contacting Geonames service")
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Geonames timezone error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/v4/geonames/brazilian-search", 
            response_description="Optimized search for Brazilian places",
            include_in_schema=True)
async def geonames_brazilian_search(
    request: Request,
    q: str,
    max_results: int = 10
):
    """
    Optimized search for Brazilian places with Portuguese localization.
    """
    write_request_to_log(20, request, f"Brazilian Geonames search for: {q}")
    
    # Check rate limiting
    if not await rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            raise HTTPException(status_code=401, detail="Geonames credentials not configured")
            
        result = await pt_br_optimizer.search_brazilian_places(q, max_results)
        
        if result is None:
            raise HTTPException(status_code=500, detail="Error contacting Geonames service")
            
        # Format Brazilian locations with Portuguese information
        if result.get('geonames'):
            formatted_geonames = []
            for geoname in result['geonames']:
                if geoname.get('countryCode') == 'BR':
                    formatted_geoname = await pt_br_optimizer.format_brazilian_location(geoname)
                    formatted_geonames.append(formatted_geoname)
                else:
                    formatted_geonames.append(geoname)
            result['geonames'] = formatted_geonames
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Brazilian Geonames search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/v4/geonames/country-info", 
            response_description="Get country information",
            include_in_schema=True)
async def geonames_country_info(
    request: Request,
    country: str
):
    """
    Get information about a specific country from Geonames.
    """
    write_request_to_log(20, request, f"Geonames country info for: {country}")
    
    # Check rate limiting
    if not await rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            raise HTTPException(status_code=401, detail="Geonames credentials not configured")
            
        result = await geonames_service.get_country_info(country)
        
        if result is None:
            raise HTTPException(status_code=500, detail="Error contacting Geonames service")
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Geonames country info error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")