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
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey(UserDB.id),
        nullable=False,
        index=True,
    )

    owner = relationship("UserDB", back_populates="projects")
    datasources = relationship("DatasourceDB", back_populates="project")
    warehouse = relationship("WarehouseDB", back_populates="project")
