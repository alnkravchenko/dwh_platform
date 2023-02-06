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


@router.post("/register")
def register(user: UserModel) -> Dict[str, str]:
    user_dict = user.dict()
    user_dict["response"] = "REGISTER"
    log.info(user_dict)
    return user_dict

