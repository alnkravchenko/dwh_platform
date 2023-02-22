import uuid

from sqlalchemy import Column, Integer, String

from .base import Base

# from sqlalchemy.dialects.postgresql import UUID


class UserDB(Base):
    __tablename__ = "Users"
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
