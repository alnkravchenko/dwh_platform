from schema.user import UserModel
from sqlalchemy.orm import Session


def verify_user(db: Session, user: UserModel) -> bool:
    return True


def verify_new_user(db: Session, user: UserModel) -> bool:
    return True
