from __future__ import annotations

import hashlib
import secrets
import uuid
from typing import Any

from fastapi import HTTPException, status

from src.config.settings import settings
from src.core.services.storage_service import StorageService


class AuthService:
    def __init__(self, storage: StorageService) -> None:
        self.storage = storage

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register(self, username: str, password: str) -> dict[str, str]:
        username_norm = username.strip().lower()
        if not username_norm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is required.",
            )

        password_hash = self._hash_password(password)

        def mutator(state: dict[str, Any]) -> dict[str, str]:
            users = state["users"]
            exists = any(user["username"] == username_norm for user in users)
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User already exists.",
                )

            user = {
                "id": str(uuid.uuid4()),
                "username": username_norm,
                "password_hash": password_hash,
                "token": secrets.token_urlsafe(24),
                "cash_balance": settings.initial_wallet_balance,
                "holdings": {},
                "watchlists": [],
            }
            users.append(user)
            return {
                "user_id": user["id"],
                "username": user["username"],
                "token": user["token"],
            }

        return self.storage.transaction(mutator)

    def login(self, username: str, password: str) -> dict[str, str]:
        username_norm = username.strip().lower()
        password_hash = self._hash_password(password)

        def mutator(state: dict[str, Any]) -> dict[str, str]:
            for user in state["users"]:
                if user["username"] == username_norm and user["password_hash"] == password_hash:
                    user["token"] = secrets.token_urlsafe(24)
                    return {
                        "user_id": user["id"],
                        "username": user["username"],
                        "token": user["token"],
                    }
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        return self.storage.transaction(mutator)

    def create_user(self, username: str) -> dict[str, str]:
        """User manager helper endpoint from PDF: creates with a default password."""
        return self.register(username=username, password="changeme123")

    def list_users(self) -> list[dict[str, str]]:
        state = self.storage.read_state()
        return [{"id": user["id"], "username": user["username"]} for user in state["users"]]

    def get_user_by_token(self, token: str) -> dict[str, Any]:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization token.",
            )

        state = self.storage.read_state()
        for user in state["users"]:
            if user.get("token") == token:
                return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

