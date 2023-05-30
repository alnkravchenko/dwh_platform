from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel


class DataTableCreate(BaseModel):
    name: str
    datasource_id: UUID
    columns: List[Dict[str, str]]

    class Config:
        orm_mode = True


class DataTableModel(DataTableCreate):
    id: UUID

    class Config:
        orm_mode = True
