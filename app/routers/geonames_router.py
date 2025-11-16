"""
Geonames API Router
Provides the API endpoints for Geonames functionality in the open-source solution
"""
from starlette.routing import Router, Route
from starlette.responses import JSONResponse
from starlette.requests import Request
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

# Initialize services
geonames_service = GeonamesService()
credential_manager = CredentialManager()
rate_limiter = RateLimiter()
pt_br_optimizer = PtBrOptimizer(geonames_service)


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

        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.error(f"Geonames status error: {str(e)}")
        return JSONResponse(content={"status": "ERROR", "detail": "Internal server error"}, status_code=500)


async def geonames_search(request: Request):
    """
    Search for places using Geonames API with built-in rate limiting and credential management.
    """
    # Extract query parameters
    q = request.query_params.get("q")
    max_rows = int(request.query_params.get("max_rows", 10))
    lang = request.query_params.get("lang", "en")
    style = request.query_params.get("style", "medium")

    write_request_to_log(20, request, f"Geonames search for: {q}")

    # Check rate limiting
    if not await rate_limiter.is_allowed():
        return JSONResponse(content={"status": "ERROR", "detail": "Rate limit exceeded"}, status_code=429)

    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            return JSONResponse(content={"status": "ERROR", "detail": "Geonames credentials not configured"}, status_code=401)

        result = await geonames_service.search(q, max_rows, lang, style)

        if result is None:
            return JSONResponse(content={"status": "ERROR", "detail": "Error contacting Geonames service"}, status_code=500)

        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Geonames search error: {str(e)}")
        return JSONResponse(content={"status": "ERROR", "detail": "Internal server error"}, status_code=500)


async def geonames_timezone(request: Request):
    """
    Get timezone information for specific coordinates using Geonames API.
    """
    # Extract query parameters
    lat = float(request.query_params.get("lat"))
    lng = float(request.query_params.get("lng"))

    write_request_to_log(20, request, f"Geonames timezone for coordinates: {lat}, {lng}")

    # Check rate limiting
    if not await rate_limiter.is_allowed():
        return JSONResponse(content={"status": "ERROR", "detail": "Rate limit exceeded"}, status_code=429)

    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            return JSONResponse(content={"status": "ERROR", "detail": "Geonames credentials not configured"}, status_code=401)

        result = await geonames_service.get_timezone(lat, lng)

        if result is None:
            return JSONResponse(content={"status": "ERROR", "detail": "Error contacting Geonames service"}, status_code=500)

        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Geonames timezone error: {str(e)}")
        return JSONResponse(content={"status": "ERROR", "detail": "Internal server error"}, status_code=500)


async def geonames_brazilian_search(request: Request):
    """
    Optimized search for Brazilian places with Portuguese localization.
    """
    # Extract query parameters
    q = request.query_params.get("q")
    max_results = int(request.query_params.get("max_results", 10))

    write_request_to_log(20, request, f"Brazilian Geonames search for: {q}")

    # Check rate limiting
    if not await rate_limiter.is_allowed():
        return JSONResponse(content={"status": "ERROR", "detail": "Rate limit exceeded"}, status_code=429)

    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            return JSONResponse(content={"status": "ERROR", "detail": "Geonames credentials not configured"}, status_code=401)

        result = await pt_br_optimizer.search_brazilian_places(q, max_results)

        if result is None:
            return JSONResponse(content={"status": "ERROR", "detail": "Error contacting Geonames service"}, status_code=500)

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

        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Brazilian Geonames search error: {str(e)}")
        return JSONResponse(content={"status": "ERROR", "detail": "Internal server error"}, status_code=500)


async def geonames_country_info(request: Request):
    """
    Get information about a specific country from Geonames.
    """
    # Extract query parameters
    country = request.query_params.get("country")

    write_request_to_log(20, request, f"Geonames country info for: {country}")

    # Check rate limiting
    if not await rate_limiter.is_allowed():
        return JSONResponse(content={"status": "ERROR", "detail": "Rate limit exceeded"}, status_code=429)

    try:
        # Check if we have valid credentials
        if not credential_manager.is_credential_valid():
            return JSONResponse(content={"status": "ERROR", "detail": "Geonames credentials not configured"}, status_code=401)

        result = await geonames_service.get_country_info(country)

        if result is None:
            return JSONResponse(content={"status": "ERROR", "detail": "Error contacting Geonames service"}, status_code=500)

        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logger.error(f"Geonames country info error: {str(e)}")
        return JSONResponse(content={"status": "ERROR", "detail": "Internal server error"}, status_code=500)


# Define routes
routes = [
    Route('/api/v4/geonames/status', geonames_status, methods=['GET']),
    Route('/api/v4/geonames/search', geonames_search, methods=['GET']),
    Route('/api/v4/geonames/timezone', geonames_timezone, methods=['GET']),
    Route('/api/v4/geonames/brazilian-search', geonames_brazilian_search, methods=['GET']),
    Route('/api/v4/geonames/country-info', geonames_country_info, methods=['GET']),
]

router = Router(routes=routes)
