import uuid

from models.datasource import DatasourceDB
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from .base import Base


class DataTableDB(Base):
    __tablename__ = "DataTables"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    name = Column(String, nullable=False)
    datasource_id = Column(
        UUID(as_uuid=True),
        ForeignKey(DatasourceDB.id, ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    columns = Column(JSONB, nullable=False)

    warehouseDatatables = relationship(
        "WarehouseDataTableDB", cascade="all, delete", back_populates="datatables"
    )
