from __future__ import annotations

from pydantic import BaseModel, Field


class QuoteResponse(BaseModel):
    symbol: str
    price: float
    timestamp: str
    currency: str = "USD"


class CandleResponse(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class CompanyInfoResponse(BaseModel):
    symbol: str
    name: str
    sector: str
    industry: str
    description: str
    website: str


class SearchResult(BaseModel):
    symbol: str
    display_name: str


class HistoryQueryParams(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    period: str = Field(default="1mo")
    interval: str = Field(default="1d")

