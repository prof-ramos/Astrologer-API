"""
    This is part of Astrologer API (C) 2023 Giacomo Battaglia
"""

import logging
import logging.config

from starlette.applications import Starlette
from starlette.routing import Mount

from .routers import main_router, geonames_router
from .config.settings import settings
from .middleware.secret_key_checker_middleware import SecretKeyCheckerMiddleware


logging.config.dictConfig(settings.LOGGING_CONFIG)

# Create Starlette application with all routes
routes = [
    Mount('/', app=main_router.router),
    Mount('/', app=geonames_router.router),
]

app = Starlette(
    debug=settings.debug,
    routes=routes,
)

#------------------------------------------------------------------------------
# Middleware
#------------------------------------------------------------------------------

if settings.debug is not True:
    app.add_middleware(
        SecretKeyCheckerMiddleware,
        secret_key_name=settings.secret_key_name,
        secret_keys=[
            settings.rapid_api_secret_key,
        ],
    )
