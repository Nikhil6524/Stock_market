from __future__ import annotations

from typing import Any

from src.core.services.market_service import MarketService
from src.core.services.portfolio_service import PortfolioService


class AnalyticsService:
    def __init__(self, market_service: MarketService, portfolio_service: PortfolioService) -> None:
        self.market_service = market_service
        self.portfolio_service = portfolio_service

    async def get_report(
        self,
        user: dict[str, Any],
        stock_symbol: str,
        history_symbol: str,
        company_symbol: str,
        period: str = "1mo",
        interval: str = "1d",
    ) -> dict[str, Any]:
        stock_price = await self.market_service.get_quote(stock_symbol)
        historical_data = await self.market_service.get_history(history_symbol, period, interval)
        company_info = await self.market_service.get_company_info(company_symbol)
        user_portfolio = await self.portfolio_service.get_portfolio(user)
        return {
            "stock_price": stock_price,
            "historical_data": historical_data,
            "company_info": company_info,
            "user_portfolio": user_portfolio,
        }

