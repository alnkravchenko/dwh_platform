from typing import List

from models.user import UserDB
from schema.user import UserModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.hashing import get_hashed_password

from .database import create_entity


def get_users(db: Session, offset: int = 0, limit: int = 100) -> List[UserDB]:
    query = select(UserDB).offset(offset).limit(limit)
    return list(db.execute(query).scalars().all())


def get_user_by_username(db: Session, username: str) -> UserDB | None:
    query = select(UserDB).where(UserDB.username == username)
    return db.execute(query).scalar()


def get_user_by_email(db: Session, user_email: str) -> UserDB | None:
    query = select(UserDB).where(UserDB.email == user_email)
    return db.execute(query).scalar()


def create_user(db: Session, user: UserModel) -> UserDB:
    hashed_password = get_hashed_password(user.password.get_secret_value())
    db_user = UserDB(
        username=user.email.name, email=user.email.email, password=hashed_password
    )
    return create_entity(db, db_user)  # type: ignore
