from __future__ import annotations

from fastapi import APIRouter, Depends

from src.api.rest.dependencies import get_current_user, get_portfolio_service
from src.schemas.portfolio import (
    FundsResponse,
    OrderResponse,
    PlaceOrderRequest,
    PortfolioResponse,
    RiskCheckRequest,
    RiskCheckResponse,
)


router = APIRouter(prefix="/trading", tags=["Trading"])


@router.get("/funds", summary="Get wallet funds", response_model=FundsResponse)
async def get_funds(current_user: dict = Depends(get_current_user)) -> FundsResponse:
    data = await get_portfolio_service().get_funds(user=current_user)
    return FundsResponse(**data)


@router.get("/portfolio", summary="Get current portfolio", response_model=PortfolioResponse)
async def get_portfolio(current_user: dict = Depends(get_current_user)) -> PortfolioResponse:
    data = await get_portfolio_service().get_portfolio(user=current_user)
    return PortfolioResponse(**data)


@router.post("/risk/check-order", summary="Check order risk", response_model=RiskCheckResponse)
async def check_order(
    payload: RiskCheckRequest,
    current_user: dict = Depends(get_current_user),
) -> RiskCheckResponse:
    data = await get_portfolio_service().check_order(
        user=current_user,
        symbol=payload.symbol,
        side=payload.side,
        quantity=payload.quantity,
        price=payload.price,
    )
    return RiskCheckResponse(**data)


@router.post("/orders", summary="Place order", response_model=OrderResponse)
async def place_order(
    payload: PlaceOrderRequest,
    current_user: dict = Depends(get_current_user),
) -> OrderResponse:
    order = await get_portfolio_service().place_order(
        user=current_user,
        symbol=payload.symbol,
        side=payload.side,
        quantity=payload.quantity,
    )
    return OrderResponse(**order)


@router.get("/orders", summary="Get order book", response_model=list[OrderResponse])
async def get_orders(current_user: dict = Depends(get_current_user)) -> list[OrderResponse]:
    orders = await get_portfolio_service().get_orders(user_id=current_user["id"])
    return [OrderResponse(**order) for order in orders]


@router.delete("/orders/{order_id}", summary="Cancel order", response_model=OrderResponse)
async def cancel_order(order_id: str, current_user: dict = Depends(get_current_user)) -> OrderResponse:
    order = await get_portfolio_service().cancel_order(
        user_id=current_user["id"],
        order_id=order_id,
    )
    return OrderResponse(**order)

