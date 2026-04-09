from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from src.api.rest.dependencies import get_analytics_service, get_current_user


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/report", summary="Combined analytics report")
async def get_report(
    stock_symbol: str = Query(default="AAPL"),
    history_symbol: str = Query(default="TCS.NS"),
    company_symbol: str = Query(default="INFY.NS"),
    period: str = Query(default="1mo"),
    interval: str = Query(default="1d"),
    current_user: dict = Depends(get_current_user),
) -> dict:
    return await get_analytics_service().get_report(
        user=current_user,
        stock_symbol=stock_symbol,
        history_symbol=history_symbol,
        company_symbol=company_symbol,
        period=period,
        interval=interval,
    )

