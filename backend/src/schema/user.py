from __future__ import annotations


from typing import Optional

from pydantic import BaseModel, NameEmail, SecretStr


class UserModel(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: NameEmail
    password: SecretStr

    class Config:
        orm_mode = True
