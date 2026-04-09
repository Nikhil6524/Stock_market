from __future__ import annotations

from pydantic import BaseModel, Field


class WatchlistCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=60)


class WatchlistAddStockRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)


class WatchlistResponse(BaseModel):
    id: str
    title: str
    stocks: list[str]

