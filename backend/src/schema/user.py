from __future__ import annotations

# import uuid
from typing import Optional

from pydantic import BaseModel


# TODO: add email validation
# TODO: add password validation
class UserModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
