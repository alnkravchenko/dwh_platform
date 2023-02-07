from typing import Dict

import structlog
from fastapi import APIRouter
from schema.user import UserModel

log = structlog.get_logger()
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(user: UserModel) -> Dict[str, str]:
    user_dict = user.dict()
    user_dict["response"] = "LOGIN"
    log.info(user_dict)
    return user_dict


@router.post("/sign_up")
def sign_up(user: UserModel) -> Dict[str, str]:
    user_dict = user.dict()
    user_dict["response"] = "SIGN UP"
    log.info(user_dict)
    return user_dict

