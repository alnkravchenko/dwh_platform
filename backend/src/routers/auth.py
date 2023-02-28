from typing import Dict, List

import structlog
from fastapi import APIRouter, Depends, Response, status
from repos.database import get_db
from repos.user import create_user, get_users
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils.verification import verify_new_user, verify_user

log = structlog.get_logger()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    user: UserModel, response: Response, db: Session = Depends(get_db)
) -> Dict[str, str | None]:
    if verify_user(db, user):
        user_dict = user.dict()
        user_dict["response"] = "LOGIN"

        log.info(user_dict)
        response.status_code = status.HTTP_200_OK
        return user_dict

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"detail": "Invalid user"}


@router.get("/users/", response_model=List[UserModel])
def get_all_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, offset, limit)


@router.post("/sign_up")
def sign_up(
    user: UserModel, response: Response, db: Session = Depends(get_db)
) -> Dict[str, str]:
    if verify_new_user(db, user):
        user_dict = user.dict()
        user_dict["response"] = "SIGN UP"

        log.info(user_dict)
        create_user(db, user)
        return user_dict

    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"detail": "Invalid data"}
