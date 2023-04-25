from datetime import datetime
from typing import Annotated, List

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from repos import users as users_db
from repos.database import get_db
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils.jwt_auth import decode_token
from utils.settings import settings

from .auth import oauth2_scheme

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=List[UserModel],
)
def get_all_users(
    token: Annotated[str, Depends(oauth2_scheme)],
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return users_db.get_users(db, offset, limit)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # process token data
    try:
        payload = decode_token(token, settings.JWT_SECRET_KEY)
        expires = payload.get("exp") or 0
        if int(expires) <= datetime.utcnow().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        log.warn(f"[AUTH] 401 {credentials_exception.detail}")
        raise credentials_exception
    # get user
    user_db = users_db.get_user_by_email(db, email)
    if user_db is None:
        log.warn(f"[AUTH] 404 User(email={email}) not found")
        raise credentials_exception
    user = UserModel.from_orm(user_db)
    log.info(f"[AUTH] 200 {user}")
    return user