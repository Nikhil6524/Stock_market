from __future__ import annotations

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class UserSummary(BaseModel):
    id: str
    username: str

