from __future__ import annotations

from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str
