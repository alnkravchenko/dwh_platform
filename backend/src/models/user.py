# import uuid

import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class UserDB(Base):
    __tablename__ = "Users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id},username={self.username},email={self.email})"
