from __future__ import annotations

from fastapi import APIRouter

from src.api.rest.dependencies import get_auth_service
from src.schemas.users import CreateUserRequest, UserSummary


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", summary="Create user (user manager service)", response_model=UserSummary)
async def create_user(payload: CreateUserRequest) -> UserSummary:
    data = get_auth_service().create_user(payload.name)
    return UserSummary(id=data["user_id"], username=data["username"])


@router.get("", summary="List users", response_model=list[UserSummary])
async def list_users() -> list[UserSummary]:
    users = get_auth_service().list_users()
    return [UserSummary(**user) for user in users]

