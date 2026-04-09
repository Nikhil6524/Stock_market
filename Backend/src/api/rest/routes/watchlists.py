from __future__ import annotations

from fastapi import APIRouter, Depends

from src.api.rest.dependencies import get_current_user, get_watchlist_service
from src.schemas.watchlist import (
    WatchlistAddStockRequest,
    WatchlistCreateRequest,
    WatchlistResponse,
)


router = APIRouter(prefix="/watchlists", tags=["Watchlists"])


@router.get("", summary="Get watchlists", response_model=list[WatchlistResponse])
async def get_watchlists(current_user: dict = Depends(get_current_user)) -> list[WatchlistResponse]:
    watchlists = get_watchlist_service().get_watchlists(user_id=current_user["id"])
    return [WatchlistResponse(**item) for item in watchlists]


@router.post("", summary="Create watchlist", response_model=WatchlistResponse)
async def create_watchlist(
    payload: WatchlistCreateRequest,
    current_user: dict = Depends(get_current_user),
) -> WatchlistResponse:
    watchlist = get_watchlist_service().create_watchlist(
        user_id=current_user["id"],
        title=payload.title,
    )
    return WatchlistResponse(**watchlist)


@router.post("/{watchlist_id}/stocks", summary="Add stock to watchlist", response_model=WatchlistResponse)
async def add_stock(
    watchlist_id: str,
    payload: WatchlistAddStockRequest,
    current_user: dict = Depends(get_current_user),
) -> WatchlistResponse:
    watchlist = get_watchlist_service().add_stock(
        user_id=current_user["id"],
        watchlist_id=watchlist_id,
        symbol=payload.symbol,
    )
    return WatchlistResponse(**watchlist)

