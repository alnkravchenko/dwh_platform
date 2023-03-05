from __future__ import annotations

# import uuid
from typing import Optional

from pydantic import BaseModel, NameEmail


# TODO: add password validation
class UserModel(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: NameEmail
    password: str

    class Config:
        orm_mode = True
