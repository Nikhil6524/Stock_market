from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass, field

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(slots=True)
class Settings:
    app_name: str = "Stock Broker API"
    app_version: str = "1.0.0"
    app_env: str = os.getenv("APP_ENV", "development")
    api_prefix: str = "/api/v1"
    initial_wallet_balance: float = 100000.0
    symbol_universe: list[str] = field(
        default_factory=lambda: [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "META",
            "NVDA",
            "NFLX",
            "AMD",
            "INTC",
            "INFY.NS",
            "TCS.NS",
            "RELIANCE.NS",
            "HDFCBANK.NS",
            "ICICIBANK.NS",
            "ZOMATO.NS",
            "SBIN.NS",
        ]
    )
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("MONGO_DB", "stock_broker")
    mongo_collection: str = os.getenv("MONGO_COLLECTION", "app_state")


settings = Settings()

