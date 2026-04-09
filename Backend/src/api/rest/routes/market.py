from __future__ import annotations

from fastapi import APIRouter, Query

from src.api.rest.dependencies import get_market_service
from src.schemas.market import CandleResponse, CompanyInfoResponse, QuoteResponse, SearchResult


router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/quote", summary="Get latest quote", response_model=QuoteResponse)
async def get_quote(symbol: str = Query(..., min_length=1, max_length=20)) -> QuoteResponse:
    data = await get_market_service().get_quote(symbol=symbol)
    return QuoteResponse(**data)


@router.get("/history", summary="Get historical candles", response_model=list[CandleResponse])
async def get_history(
    symbol: str = Query(..., min_length=1, max_length=20),
    period: str = Query(default="1mo"),
    interval: str = Query(default="1d"),
) -> list[CandleResponse]:
    candles = await get_market_service().get_history(symbol=symbol, period=period, interval=interval)
    return [CandleResponse(**candle) for candle in candles]


@router.get("/company", summary="Get company profile", response_model=CompanyInfoResponse)
async def get_company(symbol: str = Query(..., min_length=1, max_length=20)) -> CompanyInfoResponse:
    data = await get_market_service().get_company_info(symbol=symbol)
    return CompanyInfoResponse(**data)


@router.get("/search", summary="Search symbols", response_model=list[SearchResult])
async def search_symbols(q: str = Query(..., min_length=1, max_length=30)) -> list[SearchResult]:
    results = await get_market_service().search_symbols(query=q)
    return [SearchResult(**item) for item in results]

