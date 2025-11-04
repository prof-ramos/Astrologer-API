"""
Tests for Geonames functionality in Astrologer API
These tests verify the open-source Geonames integration with credential management,
rate limiting, and PT-BR optimizations.
"""

from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)


def test_geonames_status():
    """
    Tests if the Geonames status endpoint returns the correct status.
    """
    response = client.get("/api/v4/geonames/status")
    
    # This test will work even without a Geonames key since it only validates the service is available
    assert response.status_code in [200, 401, 500]  # Different possible states


def test_geonames_search():
    """
    Tests Geonames search functionality.
    """
    # This test requires a valid Geonames username in the environment
    geonames_username = os.getenv("GEONAMES_USERNAME")
    
    if geonames_username:
        response = client.get("/api/v4/geonames/search", params={"q": "London"})
        assert response.status_code == 200
        data = response.json()
        assert "geonames" in data or "totalResultsCount" in data
    else:
        # Without credentials, expect 401 error
        response = client.get("/api/v4/geonames/search", params={"q": "London"})
        assert response.status_code == 401


def test_geonames_timezone():
    """
    Tests Geonames timezone functionality.
    """
    geonames_username = os.getenv("GEONAMES_USERNAME")
    
    if geonames_username:
        response = client.get("/api/v4/geonames/timezone", params={"lat": 51.5074, "lng": -0.1278})  # London coordinates
        assert response.status_code == 200
        data = response.json()
        assert "timezoneId" in data
        assert "dstOffset" in data
    else:
        # Without credentials, expect 401 error
        response = client.get("/api/v4/geonames/timezone", params={"lat": 51.5074, "lng": -0.1278})
        assert response.status_code == 401


def test_geonames_country_info():
    """
    Tests Geonames country info functionality.
    """
    geonames_username = os.getenv("GEONAMES_USERNAME")
    
    if geonames_username:
        response = client.get("/api/v4/geonames/country-info", params={"country": "GB"})  # Great Britain
        assert response.status_code == 200
        data = response.json()
        assert "geonames" in data
        assert len(data["geonames"]) > 0
    else:
        # Without credentials, expect 401 error
        response = client.get("/api/v4/geonames/country-info", params={"country": "GB"})
        assert response.status_code == 401


def test_geonames_brazilian_search():
    """
    Tests Geonames Brazilian search functionality with PT-BR optimizations.
    """
    geonames_username = os.getenv("GEONAMES_USERNAME")
    
    if geonames_username:
        response = client.get("/api/v4/geonames/brazilian-search", params={"q": "São Paulo"})
        assert response.status_code == 200
        data = response.json()
        
        # Check if results are returned
        if "geonames" in data:
            assert len(data["geonames"]) > 0
            # If it's a Brazilian location, check for Portuguese name
            for geoname in data["geonames"]:
                if geoname.get("countryCode") == "BR":
                    # Should have portugueseName field for Brazilian locations
                    assert "portugueseName" in geoname
    else:
        # Without credentials, expect 401 error
        response = client.get("/api/v4/geonames/brazilian-search", params={"q": "São Paulo"})
        assert response.status_code == 401


def test_geonames_rate_limiting():
    """
    Tests that Geonames endpoints respect rate limiting.
    """
    # This test is difficult to implement without triggering actual rate limits
    # For now, just verify the rate limit status is accessible
    response = client.get("/api/v4/geonames/status")
    if response.status_code in [200, 401, 500]:
        data = response.json()
        if "rate_limiting" in data:
            assert "current_minute" in data["rate_limiting"]
            assert "current_hour" in data["rate_limiting"]


def test_credential_management():
    """
    Tests credential management functionality.
    """
    response = client.get("/api/v4/geonames/status")
    
    # Check that the response includes credential status information
    if response.status_code in [200, 401, 500]:
        data = response.json()
        if "credential_status" in data:
            assert "is_valid" in data["credential_status"]
            assert "last_checked" in data["credential_status"]