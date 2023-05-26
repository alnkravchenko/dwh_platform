import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base
from .user import UserDB


class ProjectDB(Base):
    __tablename__ = "Projects"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    name = Column(String, nullable=False)
    node_url = Column(String, nullable=False)
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey(UserDB.id, ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    owner = relationship(UserDB, back_populates="projects")
    datasources = relationship(
        "DatasourceDB", cascade="all, delete", back_populates="project"
    )
    warehouse = relationship(
        "WarehouseDB", cascade="all, delete", back_populates="project"
    )
