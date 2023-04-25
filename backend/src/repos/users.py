from typing import List

from models.user import UserDB
from schema.user import UserCreate, UserModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.hashing import get_hashed_password

from .database import create_entity


def get_users(db: Session, offset: int = 0, limit: int = 100) -> List[UserModel]:
    query = select(UserDB).offset(offset).limit(limit)
    users = db.execute(query).scalars().all()
    db.commit()
    return list(map(UserModel.from_orm, users))


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    query = select(UserDB).where(UserDB.username == username)
    user_db = db.execute(query).scalar()
    db.commit()
    if user_db is not None:
        return UserModel.from_orm(user_db)


def get_user_by_email(db: Session, user_email: str) -> UserModel | None:
    query = select(UserDB).where(UserDB.email == user_email)
    user_db = db.execute(query).scalar()
    db.commit()
    if user_db is not None:
        return UserModel.from_orm(user_db)


def create_user(db: Session, user: UserCreate) -> UserModel:
    hashed_password = get_hashed_password(user.password.get_secret_value())
    user_db = UserDB(
        username=user.email.name, email=user.email.email, password=hashed_password
    )
    return UserModel.from_orm(create_entity(db, user_db))
