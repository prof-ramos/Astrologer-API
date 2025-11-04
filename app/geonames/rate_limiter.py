"""
Rate Limiting System for Geonames API
Implements rate limiting to prevent exceeding Geonames API limits in the open-source solution
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from collections import defaultdict
import time


logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Implements rate limiting for Geonames API calls to prevent exceeding usage limits
    in the open-source solution.
    """
    
    def __init__(self, requests_per_minute: int = 2000, requests_per_hour: int = 10000):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests_by_minute: Dict[str, int] = defaultdict(int)
        self.requests_by_hour: Dict[str, int] = defaultdict(int)
        self.request_timestamps: list = []
        self._lock = asyncio.Lock()
        
    def _cleanup_old_requests(self):
        """Remove requests older than the time windows"""
        now = time.time()
        # Keep only requests from the last hour
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < 3600]
        
    def _get_minute_key(self) -> str:
        """Get the key for the current minute"""
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}"
        
    def _get_hour_key(self) -> str:
        """Get the key for the current hour"""
        now = datetime.now()
        return f"{now.year}-{now.month}-{now.day}-{now.hour}"
        
    async def is_allowed(self) -> bool:
        """Check if a new request is allowed under rate limits"""
        async with self._lock:
            now = time.time()
            current_minute = self._get_minute_key()
            current_hour = self._get_hour_key()
            
            # Cleanup old requests
            self._cleanup_old_requests()
            
            # Count requests in the current minute and hour
            minute_count = len([ts for ts in self.request_timestamps if now - ts <= 60])
            hour_count = len([ts for ts in self.request_timestamps if now - ts <= 3600])
            
            # Check if limits are exceeded
            if minute_count >= self.requests_per_minute:
                logger.warning(f"Rate limit exceeded: {minute_count}/{self.requests_per_minute} requests in the last minute")
                return False
                
            if hour_count >= self.requests_per_hour:
                logger.warning(f"Rate limit exceeded: {hour_count}/{self.requests_per_hour} requests in the last hour")
                return False
                
            # Record this request
            self.request_timestamps.append(now)
            self.requests_by_minute[current_minute] = self.requests_by_minute[current_minute] + 1
            self.requests_by_hour[current_hour] = self.requests_by_hour[current_hour] + 1
            
            return True
            
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        async with self._lock:
            now = time.time()
            current_minute = self._get_minute_key()
            current_hour = self._get_hour_key()
            
            self._cleanup_old_requests()
            
            minute_count = len([ts for ts in self.request_timestamps if now - ts <= 60])
            hour_count = len([ts for ts in self.request_timestamps if now - ts <= 3600])
            
            return {
                "current_minute": {
                    "count": minute_count,
                    "limit": self.requests_per_minute,
                    "remaining": max(0, self.requests_per_minute - minute_count),
                    "percent_used": (minute_count / self.requests_per_minute) * 100 if self.requests_per_minute > 0 else 0
                },
                "current_hour": {
                    "count": hour_count,
                    "limit": self.requests_per_hour,
                    "remaining": max(0, self.requests_per_hour - hour_count),
                    "percent_used": (hour_count / self.requests_per_hour) * 100 if self.requests_per_hour > 0 else 0
                }
            }