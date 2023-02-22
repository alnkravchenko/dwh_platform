from __future__ import annotations

import uuid

from pydantic import BaseModel


# TODO: add email validation
# TODO: add password validation
class UserModel(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
