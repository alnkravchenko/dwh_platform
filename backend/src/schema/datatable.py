from typing import Dict
from uuid import UUID

from pydantic import BaseModel


class DataTableCreate(BaseModel):
    name: str
    ds_id: UUID
    fields: Dict[str, str]

    class Config:
        orm_mode = True


class DataTableModel(DataTableCreate):
    id: UUID

    class Config:
        orm_mode = True
