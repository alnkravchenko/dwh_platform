from typing import Annotated, List

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from repos import users as users_db
from repos.database import get_db
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils.jwt_auth import decode_token
from utils.settings import settings

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # process token data
    try:
        payload = decode_token(token, settings.JWT_SECRET_KEY)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # get user
    user_db = users_db.get_user_by_email(db, email)
    if user_db is None:
        raise credentials_exception
    user = UserModel.from_orm(user_db)
    return user
