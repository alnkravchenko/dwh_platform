from repos import user as user_db
from schema.user import UserModel
from sqlalchemy.orm import Session


def verify_user(db: Session, user: UserModel) -> bool:
    user_entities = user_db.get_user_by_email(db, user)
    if len(user_entities) == 1:
        return user.password == user_entities[0].password
    return False


def verify_new_user(db: Session, user: UserModel) -> bool:
    users_by_username = user_db.get_user_by_username(db, user)
    users_by_email = user_db.get_user_by_email(db, user)
    return len(users_by_username) + len(users_by_email) == 0
