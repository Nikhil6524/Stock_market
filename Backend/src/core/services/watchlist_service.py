from __future__ import annotations

import uuid
from typing import Any

from fastapi import HTTPException, status

from src.core.services.storage_service import StorageService


class WatchlistService:
    def __init__(self, storage: StorageService) -> None:
        self.storage = storage

    def get_watchlists(self, user_id: str) -> list[dict[str, Any]]:
        state = self.storage.read_state()
        for user in state["users"]:
            if user["id"] == user_id:
                return user.get("watchlists", [])
        return []

    def create_watchlist(self, user_id: str, title: str) -> dict[str, Any]:
        clean_title = title.strip()
        if not clean_title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Watchlist title is required.",
            )

        def mutator(state: dict[str, Any]) -> dict[str, Any]:
            for user in state["users"]:
                if user["id"] != user_id:
                    continue

                watchlists = user.setdefault("watchlists", [])
                exists = any(w["title"].lower() == clean_title.lower() for w in watchlists)
                if exists:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Watchlist already exists.",
                    )

                watchlist = {"id": str(uuid.uuid4()), "title": clean_title, "stocks": []}
                watchlists.append(watchlist)
                return watchlist

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return self.storage.transaction(mutator)

    def add_stock(self, user_id: str, watchlist_id: str, symbol: str) -> dict[str, Any]:
        ticker = symbol.strip().upper()
        if not ticker:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock symbol is required.",
            )

        def mutator(state: dict[str, Any]) -> dict[str, Any]:
            for user in state["users"]:
                if user["id"] != user_id:
                    continue

                watchlists = user.setdefault("watchlists", [])
                for watchlist in watchlists:
                    if watchlist["id"] == watchlist_id:
                        stocks: list[str] = watchlist.setdefault("stocks", [])
                        if ticker not in stocks:
                            stocks.append(ticker)
                        return watchlist

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Watchlist not found.",
                )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return self.storage.transaction(mutator)

