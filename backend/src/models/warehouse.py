import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base
from .project import ProjectDB


class WarehouseDB(Base):
    __tablename__ = "Warehouses"
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

    project = relationship(ProjectDB, back_populates="warehouse")
    # datatables = relationship(
    #     "WarehouseDataTableDB", cascade="all,delete", back_populates="warehouse"
    # )
