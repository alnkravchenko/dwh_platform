from pydantic import BaseModel

from .jwt_auth import Token


class DefaultResponse(BaseModel):
    details: str


class TokenResponse(DefaultResponse):
    token: Token
