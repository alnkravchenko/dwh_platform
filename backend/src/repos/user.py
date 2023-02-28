from typing import List

from models.base import Base
from models.user import UserDB
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils.hashing import get_hashed_password


def get_users(db: Session, offset: int = 0, limit: int = 100) -> List[UserDB]:
    return db.query(UserDB).offset(offset).limit(limit).all()


def get_user_by_username(db: Session, user: UserModel) -> UserDB | None:
    return db.query(UserDB).filter_by(username=user.username).first()


def get_user_by_email(db: Session, user: UserModel) -> UserDB | None:
    return db.query(UserDB).filter_by(email=user.email).first()


def create_user(db: Session, user: UserModel) -> UserDB:
    hashed_password = get_hashed_password(user.password)
    db_user = UserDB(username=user.username, email=user.email, password=hashed_password)
    return create_entity(db, db_user)  # type: ignore


def create_entity(db: Session, entity: Base) -> Base:
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity
