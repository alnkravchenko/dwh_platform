from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, NameEmail, SecretStr


class UserCreate(BaseModel):
    email: NameEmail
    password: SecretStr

    class Config:
        orm_mode = True


class UserModel(UserCreate):
    id: UUID
    username: str

    class Config:
        orm_mode = True
