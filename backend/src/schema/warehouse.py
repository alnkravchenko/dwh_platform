from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class WarehouseCreate(BaseModel):
    name: str
    datatables: List[UUID]
    project_id: UUID

    class Config:
        orm_mode = True


class WarehouseModel(WarehouseCreate):
    id: UUID

    class Config:
        orm_mode = True


class WarehouseUpdate(BaseModel):
    name: Optional[str]
    datatables: Optional[List[UUID]]

    class Config:
        orm_mode = True
