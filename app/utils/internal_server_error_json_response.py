"""
    This is part of Astrologer API (C) 2023 Giacomo Battaglia
"""

from starlette.responses import JSONResponse

InternalServerErrorJsonResponse = JSONResponse(
    status_code=500,
    content={
        "message": "Internal Server Error",
        "status": "KO",
    },
)
