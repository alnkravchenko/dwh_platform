from typing import Tuple

from repos import users as user_db
from schema.user import UserCreate
from sqlalchemy.orm import Session

from .hashing import check_password


def verify_user(db: Session, user: UserCreate) -> Tuple[bool, str]:
    user_entity = user_db.get_user_by_email(db, user.email.email)
    if user_entity is not None:
        password_verification = check_password(
            user.password.get_secret_value(), str(user_entity.password)
        )
        response_msg = (
            "User verified"
            if password_verification
            else "Value is not a valid password"
        )
        return password_verification, response_msg
    return False, "No user found by email"


def verify_new_user(db: Session, user: UserCreate) -> Tuple[bool, str]:
    user_by_email = user_db.get_user_by_email(db, user.email.email)
    user_verification = user_by_email is None
    msg = (
        "New user created"
        if user_verification
        else "User with this email has already exist"
    )
    return user_verification, msg
