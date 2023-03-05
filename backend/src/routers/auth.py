from typing import List

import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from repos.database import get_db
from repos.user import create_user, get_users
from schema.responses import DefaultResponse
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils.verification import verify_new_user, verify_user

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    responses={200: {"model": DefaultResponse}, 401: {"model": DefaultResponse}},
)
def login(user: UserModel, db: Session = Depends(get_db)) -> JSONResponse:
    is_verified, msg = verify_user(db, user)
    status_code = 200 if is_verified else 401
    log.info(f"[LOGIN] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.get("/users/", response_model=List[UserModel])
def get_all_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, offset, limit)


@router.post(
    "/sign_up",
    responses={201: {"model": DefaultResponse}, 400: {"model": DefaultResponse}},
)
def sign_up(user: UserModel, db: Session = Depends(get_db)) -> JSONResponse:
    is_verified, msg = verify_new_user(db, user)
    if is_verified:
        create_user(db, user)
    status_code = 201 if is_verified else 400
    log.info(f"[SIGN UP] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)
