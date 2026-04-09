from __future__ import annotations

from copy import deepcopy
from threading import Lock
from typing import Any, Callable

from pymongo import MongoClient

from src.config.settings import settings


StateMutator = Callable[[dict[str, Any]], Any]


class StorageService:
    """MongoDB-backed storage for a lightweight local project setup."""

    def __init__(self, mongo_uri: str, db_name: str, collection_name: str) -> None:
        self._client = MongoClient(mongo_uri)
        self._collection = self._client[db_name][collection_name]
        self._lock = Lock()
        self._ensure_initialized()

    def _default_state(self) -> dict[str, Any]:
        return {
            "users": [],
            "orders": [],
            "symbol_universe": settings.symbol_universe,
        }

    def _ensure_initialized(self) -> None:
        if self._collection.find_one({"_id": "state"}) is None:
            self._collection.insert_one({"_id": "state", **self._default_state()})

    def read_state(self) -> dict[str, Any]:
        with self._lock:
            data = self._collection.find_one({"_id": "state"})
            if data is None:
                data = {"_id": "state", **self._default_state()}
                self._collection.insert_one(data)
            state = deepcopy(data)
            state.pop("_id", None)
            return state

    def transaction(self, mutator: StateMutator) -> Any:
        with self._lock:
            data = self._collection.find_one({"_id": "state"})
            if data is None:
                data = {"_id": "state", **self._default_state()}

            state = deepcopy(data)
            state.pop("_id", None)
            result = mutator(state)
            self._collection.replace_one({"_id": "state"}, {"_id": "state", **state}, upsert=True)
            return result

