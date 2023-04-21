from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt

from .settings import settings

ALGORITHM = "HS256"


def _create_token_template(
    subject: str | Any,
    expires_setting: int,
    secret_key: str,
    expires_delta=None,
) -> str:
    # get deadline when token is expired
    delta = expires_delta or expires_setting
    token_deadline = datetime.utcnow() + timedelta(minutes=delta)
    # create token
    jwt_dict = {"exp": token_deadline, "sub": str(subject)}
    encoded_jwt = jwt.encode(jwt_dict, secret_key, ALGORITHM)
    return encoded_jwt


def create_access_token(subject: str | Any, expires_delta=None) -> str:
    return _create_token_template(
        subject,
        settings.ACCESS_TOKEN_EXPIRE_MIN,
        settings.JWT_SECRET_KEY,
        expires_delta,
    )


def decode_token(token: str, secret_key: str) -> Dict[str, str | Any]:
    return jwt.decode(token, secret_key, algorithms=[ALGORITHM])
