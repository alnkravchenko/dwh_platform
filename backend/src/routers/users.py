import structlog
from fastapi import Depends, HTTPException
from jose import ExpiredSignatureError, JWTError
from repos import users as users_db
from repos.database import get_db
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils.jwt_auth import decode_token
from utils.settings import settings

from .auth import oauth2_scheme

log = structlog.get_logger(module=__name__)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # process token data
    try:
        payload = decode_token(token, settings.JWT_SECRET_KEY)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except HTTPException as err:
        log.warn(f"[AUTH] {err.status_code} {err.detail}")
        raise err
    except ExpiredSignatureError:
        log.warn("[AUTH] 401 Signature has expired")
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as err:
        log.warn(f"[AUTH] 401 {err}")
        raise credentials_exception
    # get user
    user_db = users_db.get_user_by_email(db, email)
    if user_db is None:
        log.warn(f"[AUTH] 404 User(email={email}) not found")
        raise credentials_exception
    user = UserModel.from_orm(user_db)
    log.info(f"[AUTH] 200 {user}")
    return user
