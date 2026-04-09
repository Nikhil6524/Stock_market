from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import Header, HTTPException, status

from src.config.settings import settings
from src.core.services.analytics_service import AnalyticsService
from src.core.services.auth_service import AuthService
from src.core.services.market_service import MarketService
from src.core.services.portfolio_service import PortfolioService
from src.core.services.risk_service import RiskService
from src.core.services.storage_service import StorageService
from src.core.services.watchlist_service import WatchlistService


@lru_cache
def get_storage_service() -> StorageService:
    return StorageService(
        mongo_uri=settings.mongo_uri,
        db_name=settings.mongo_db,
        collection_name=settings.mongo_collection,
    )


@lru_cache
def get_auth_service() -> AuthService:
    return AuthService(storage=get_storage_service())


@lru_cache
def get_market_service() -> MarketService:
    return MarketService()


@lru_cache
def get_risk_service() -> RiskService:
    return RiskService()


@lru_cache
def get_watchlist_service() -> WatchlistService:
    return WatchlistService(storage=get_storage_service())


@lru_cache
def get_portfolio_service() -> PortfolioService:
    return PortfolioService(
        storage=get_storage_service(),
        market_service=get_market_service(),
        risk_service=get_risk_service(),
    )


@lru_cache
def get_analytics_service() -> AnalyticsService:
    return AnalyticsService(
        market_service=get_market_service(),
        portfolio_service=get_portfolio_service(),
    )


def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required.",
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must be in 'Bearer <token>' format.",
        )

    token = authorization.removeprefix("Bearer ").strip()
    return get_auth_service().get_user_by_token(token=token)

