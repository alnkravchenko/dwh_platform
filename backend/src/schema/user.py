from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, NameEmail, SecretStr


class UserModel(BaseModel):
    id: Optional[UUID]
    username: Optional[str]
    email: NameEmail
    password: SecretStr

    class Config:
        orm_mode = True
