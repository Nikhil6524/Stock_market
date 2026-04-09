from __future__ import annotations

from typing import Any

from anyio import to_thread
from fastapi import HTTPException, status

from src.config.settings import settings

try:
    import yfinance as yf
except ImportError:  # pragma: no cover - handled at runtime
    yf = None


class MarketService:
    def __init__(self) -> None:
        if yf is None:
            raise RuntimeError(
                "yfinance is not installed. Install dependencies from Backend/requirements.txt."
            )

    @staticmethod
    def _to_symbol(symbol: str) -> str:
        return symbol.strip().upper()

    async def get_quote(self, symbol: str) -> dict[str, Any]:
        ticker_symbol = self._to_symbol(symbol)

        def _fetch() -> dict[str, Any]:
            ticker = yf.Ticker(ticker_symbol)
            price = None
            currency = "USD"
            timestamp = ""

            try:
                info = ticker.fast_info
                price = info.get("last_price") or info.get("regular_market_price")
                currency = info.get("currency", "USD") or "USD"
            except Exception:
                price = None

            history = ticker.history(period="1d", interval="1m")
            if not history.empty:
                last_row = history.tail(1).iloc[0]
                price = float(last_row["Close"]) if price is None else float(price)
                timestamp = history.tail(1).index[0].isoformat()

            if price is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Unable to fetch quote for symbol '{ticker_symbol}'.",
                )

            return {
                "symbol": ticker_symbol,
                "price": round(float(price), 4),
                "timestamp": timestamp,
                "currency": currency,
            }

        return await to_thread.run_sync(_fetch)

    async def get_history(self, symbol: str, period: str, interval: str) -> list[dict[str, Any]]:
        ticker_symbol = self._to_symbol(symbol)

        def _fetch() -> list[dict[str, Any]]:
            ticker = yf.Ticker(ticker_symbol)
            history = ticker.history(period=period, interval=interval)
            if history.empty:
                return []

            rows: list[dict[str, Any]] = []
            for index, row in history.iterrows():
                rows.append(
                    {
                        "date": index.isoformat(),
                        "open": round(float(row["Open"]), 4),
                        "high": round(float(row["High"]), 4),
                        "low": round(float(row["Low"]), 4),
                        "close": round(float(row["Close"]), 4),
                        "volume": int(row["Volume"]),
                    }
                )
            return rows

        return await to_thread.run_sync(_fetch)

    async def get_company_info(self, symbol: str) -> dict[str, Any]:
        ticker_symbol = self._to_symbol(symbol)

        def _fetch() -> dict[str, Any]:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info or {}
            return {
                "symbol": ticker_symbol,
                "name": info.get("longName") or ticker_symbol,
                "sector": info.get("sector") or "N/A",
                "industry": info.get("industry") or "N/A",
                "description": info.get("longBusinessSummary") or "N/A",
                "website": info.get("website") or "N/A",
            }

        return await to_thread.run_sync(_fetch)

    async def search_symbols(self, query: str) -> list[dict[str, str]]:
        term = query.strip().upper()
        if not term:
            return []

        results: list[dict[str, str]] = []
        for symbol in settings.symbol_universe:
            if term in symbol.upper():
                results.append({"symbol": symbol, "display_name": symbol})
        return results[:10]

