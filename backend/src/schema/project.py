from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .datasource import DatasourceModel
from .warehouse import WarehouseModel


class ProjectCreate(BaseModel):
    name: str
    created_by: UUID

    class Config:
        orm_mode = True


class ProjectModel(ProjectCreate):
    id: UUID

    class Config:
        orm_mode = True


class ProjectContent(BaseModel):
    id: UUID
    warehouse: Optional[WarehouseModel]
    datasources: List[DatasourceModel]

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True
