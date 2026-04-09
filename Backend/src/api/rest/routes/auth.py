from __future__ import annotations

from fastapi import APIRouter

from src.api.rest.dependencies import get_auth_service
from src.schemas.auth import AuthResponse, LoginRequest, RegisterRequest


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", summary="Register user", response_model=AuthResponse)
async def register(payload: RegisterRequest) -> AuthResponse:
    data = get_auth_service().register(payload.username, payload.password)
    return AuthResponse(**data)


@router.post("/login", summary="Login user", response_model=AuthResponse)
async def login(payload: LoginRequest) -> AuthResponse:
    data = get_auth_service().login(payload.username, payload.password)
    return AuthResponse(**data)

