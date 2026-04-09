from __future__ import annotations

from fastapi import FastAPI

from src.api.middleware.cors import add_cors
from src.api.middleware.error_handler import add_error_handlers
from src.api.rest.routes.analytics import router as analytics_router
from src.api.rest.routes.auth import router as auth_router
from src.api.rest.routes.health import router as health_router
from src.api.rest.routes.market import router as market_router
from src.api.rest.routes.trading import router as trading_router
from src.api.rest.routes.users import router as users_router
from src.api.rest.routes.watchlists import router as watchlists_router
from src.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "FastAPI-based stock broker demo using yfinance, with virtual wallet, "
            "watchlists, risk checks, and order management."
        ),
    )

    add_cors(app)
    add_error_handlers(app)

    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(auth_router, prefix=settings.api_prefix)
    app.include_router(users_router, prefix=settings.api_prefix)
    app.include_router(market_router, prefix=settings.api_prefix)
    app.include_router(watchlists_router, prefix=settings.api_prefix)
    app.include_router(trading_router, prefix=settings.api_prefix)
    app.include_router(analytics_router, prefix=settings.api_prefix)

    return app


app = create_app()

