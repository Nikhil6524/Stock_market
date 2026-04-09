from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status

from src.core.services.market_service import MarketService
from src.core.services.risk_service import RiskService
from src.core.services.storage_service import StorageService


class PortfolioService:
    def __init__(
        self,
        storage: StorageService,
        market_service: MarketService,
        risk_service: RiskService,
    ) -> None:
        self.storage = storage
        self.market_service = market_service
        self.risk_service = risk_service

    async def get_funds(self, user: dict[str, Any]) -> dict[str, float]:
        return {"available_cash": round(float(user.get("cash_balance", 0.0)), 2)}

    async def get_portfolio(self, user: dict[str, Any]) -> dict[str, Any]:
        holdings_dict: dict[str, dict[str, Any]] = user.get("holdings", {})

        async def resolve_holding(symbol: str, data: dict[str, Any]) -> dict[str, Any]:
            quantity = int(data.get("quantity", 0))
            average_price = float(data.get("average_price", 0.0))
            try:
                quote = await self.market_service.get_quote(symbol)
                current_price = float(quote["price"])
            except Exception:
                current_price = average_price

            market_value = quantity * current_price
            return {
                "symbol": symbol,
                "quantity": quantity,
                "average_price": round(average_price, 4),
                "current_price": round(current_price, 4),
                "market_value": round(market_value, 4),
            }

        tasks = [resolve_holding(symbol, data) for symbol, data in holdings_dict.items()]
        holdings = await asyncio.gather(*tasks) if tasks else []
        total_stock_value = sum(item["market_value"] for item in holdings)
        cash_balance = float(user.get("cash_balance", 0.0))

        return {
            "holdings": holdings,
            "cash_balance": round(cash_balance, 2),
            "total_stock_value": round(total_stock_value, 2),
            "total_value": round(cash_balance + total_stock_value, 2),
        }

    async def check_order(
        self,
        user: dict[str, Any],
        symbol: str,
        side: str,
        quantity: int,
        price: float,
    ) -> dict[str, Any]:
        is_valid, message, errors = self.risk_service.check_order(
            user=user,
            side=side,
            symbol=symbol,
            quantity=quantity,
            price=price,
        )
        return {"is_valid": is_valid, "message": message, "errors": errors}

    async def place_order(
        self,
        user: dict[str, Any],
        symbol: str,
        side: str,
        quantity: int,
    ) -> dict[str, Any]:
        ticker = symbol.strip().upper()
        quote = await self.market_service.get_quote(ticker)
        price = float(quote["price"])
        risk = await self.check_order(user, ticker, side, quantity, price)

        if not risk["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=risk,
            )

        total_amount = round(quantity * price, 4)

        def mutator(state: dict[str, Any]) -> dict[str, Any]:
            found_user: dict[str, Any] | None = None
            for state_user in state["users"]:
                if state_user["id"] == user["id"]:
                    found_user = state_user
                    break

            if found_user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found.",
                )

            holdings: dict[str, dict[str, Any]] = found_user.setdefault("holdings", {})
            cash_balance = float(found_user.get("cash_balance", 0.0))
            position = holdings.get(ticker, {"quantity": 0, "average_price": 0.0})
            old_qty = int(position.get("quantity", 0))
            old_avg = float(position.get("average_price", 0.0))

            if side == "BUY":
                new_qty = old_qty + quantity
                new_avg = ((old_qty * old_avg) + total_amount) / new_qty if new_qty else 0.0
                holdings[ticker] = {"quantity": new_qty, "average_price": round(new_avg, 4)}
                found_user["cash_balance"] = round(cash_balance - total_amount, 4)
            else:
                new_qty = old_qty - quantity
                if new_qty <= 0:
                    holdings.pop(ticker, None)
                else:
                    holdings[ticker] = {"quantity": new_qty, "average_price": old_avg}
                found_user["cash_balance"] = round(cash_balance + total_amount, 4)

            order = {
                "id": str(uuid.uuid4()),
                "user_id": found_user["id"],
                "symbol": ticker,
                "side": side,
                "quantity": quantity,
                "price": round(price, 4),
                "total_amount": total_amount,
                "status": "FILLED",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            state["orders"].append(order)
            return order

        return self.storage.transaction(mutator)

    async def get_orders(self, user_id: str) -> list[dict[str, Any]]:
        state = self.storage.read_state()
        orders = [order for order in state["orders"] if order["user_id"] == user_id]
        return sorted(orders, key=lambda item: item["created_at"], reverse=True)

    async def cancel_order(self, user_id: str, order_id: str) -> dict[str, Any]:
        def mutator(state: dict[str, Any]) -> dict[str, Any]:
            for order in state["orders"]:
                if order["id"] == order_id and order["user_id"] == user_id:
                    if order["status"] != "OPEN":
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only OPEN orders can be cancelled.",
                        )
                    order["status"] = "CANCELLED"
                    return order
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        return self.storage.transaction(mutator)

