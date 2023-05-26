import uuid

from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base
from .datatable import DataTableDB
from .warehouse import WarehouseDB


class WarehouseDataTableDB(Base):
    __tablename__ = "WarehouseDatatables"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    warehouse_id = Column(
        UUID(as_uuid=True),
        ForeignKey(WarehouseDB.id, ondelete="CASCADE"),
        nullable=False,
    )
    datatable_id = Column(
        UUID(as_uuid=True),
        ForeignKey(DataTableDB.id, ondelete="CASCADE"),
        nullable=False,
    )
    dt_type = Column(
        Enum(
            "fact_table",
            "dimension_table",
            name="datatable_type",
        ),
        nullable=False,
    )

    warehouse = relationship(WarehouseDB, back_populates="datatables")
    datatables = relationship(DataTableDB, back_populates="warehouse")
