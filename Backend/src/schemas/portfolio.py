from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class HoldingResponse(BaseModel):
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    market_value: float


class PortfolioResponse(BaseModel):
    holdings: list[HoldingResponse]
    cash_balance: float
    total_stock_value: float
    total_value: float


class FundsResponse(BaseModel):
    available_cash: float


class PlaceOrderRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    side: Literal["BUY", "SELL"]
    quantity: int = Field(gt=0, le=100000)


class OrderResponse(BaseModel):
    id: str
    user_id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    quantity: int
    price: float
    total_amount: float
    status: str
    created_at: str


class RiskCheckRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    side: Literal["BUY", "SELL"]
    quantity: int = Field(gt=0, le=100000)
    price: float = Field(gt=0)


class RiskCheckResponse(BaseModel):
    is_valid: bool
    message: str
    errors: list[str] = []

