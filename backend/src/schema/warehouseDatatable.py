from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class DatatableType(str, Enum):
    FACT = "fact"
    DIMENSION = "dimension"


class WarehouseDataTableCreate(BaseModel):
    warehouse_id: UUID
    datatable_id: UUID
    dt_type: DatatableType

    class Config:
        orm_mode = True


class WarehouseDataTableModel(WarehouseDataTableCreate):
    id: UUID

    class Config:
        orm_mode = True
