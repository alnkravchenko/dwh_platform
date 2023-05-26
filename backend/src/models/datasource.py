import uuid

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .base import Base
from .project import ProjectDB


class DatasourceDB(Base):
    __tablename__ = "Datasources"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    name = Column(String, nullable=False)
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey(ProjectDB.id, ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ds_type = Column(
        Enum("mysql", "postgresql", "mongodb", "file", "api", name="datasource_type"),
        nullable=False,
    )
    config = Column(JSONB, nullable=False)

    project = relationship("ProjectDB", back_populates="datasources")
