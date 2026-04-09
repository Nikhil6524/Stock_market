from __future__ import annotations

from typing import Any


class RiskService:
    def check_order(
        self,
        user: dict[str, Any],
        side: str,
        symbol: str,
        quantity: int,
        price: float,
    ) -> tuple[bool, str, list[str]]:
        errors: list[str] = []
        total_amount = quantity * price
        holdings = user.get("holdings", {})
        position = holdings.get(symbol, {"quantity": 0})
        owned_quantity = int(position.get("quantity", 0))

        if side == "BUY" and float(user.get("cash_balance", 0.0)) < total_amount:
            errors.append("Insufficient funds.")

        if side == "SELL" and owned_quantity < quantity:
            errors.append("Insufficient holdings to sell.")

        if quantity <= 0:
            errors.append("Quantity must be greater than zero.")

        if price <= 0:
            errors.append("Price must be greater than zero.")

        is_valid = len(errors) == 0
        message = "Order is valid." if is_valid else "Order is invalid."
        return is_valid, message, errors

