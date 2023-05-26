from __future__ import annotations

from string import ascii_letters, digits
from typing import Tuple
from uuid import UUID

from pydantic import BaseModel, NameEmail, SecretStr


class UserCreate(BaseModel):
    email: NameEmail
    password: SecretStr

    @classmethod
    def validate_password(cls, value: SecretStr) -> Tuple[bool, str]:
        pwd = value.get_secret_value()
        msgs = []
        if len(pwd) < 8:
            msgs.append("be at least 8 characters long")
        if any(char.isspace() for char in pwd):
            msgs.append("not contain spaces")
        if not any(char.isupper() for char in pwd):
            msgs.append("contain an uppercase letter")
        if not any(char.isdecimal() for char in pwd):
            msgs.append("contain a number")
        if set(pwd).difference(ascii_letters + digits):
            msgs.append("not contain any special characters (!@#$%^&*()-+?_=,<>/)")

        if msgs:
            return False, f"Password must: {', '.join(msgs)}"
        return True, "Password is valid"

    class Config:
        orm_mode = True


class UserModel(UserCreate):
    id: UUID
    username: str

    class Config:
        orm_mode = True
