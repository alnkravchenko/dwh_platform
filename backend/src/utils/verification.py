from repos import user as user_db
from schema.user import UserModel
from sqlalchemy.orm import Session

from .hashing import check_password


def verify_user(db: Session, user: UserModel) -> bool:
    user_entity = user_db.get_user_by_email(db, user)
    if user_entity is not None:
        return check_password(user.password, str(user_entity.password))
    return False


def verify_new_user(db: Session, user: UserModel) -> bool:
    user_by_username = user_db.get_user_by_username(db, user)
    user_by_email = user_db.get_user_by_email(db, user)
    return user_by_username is not None and user_by_email is not None
