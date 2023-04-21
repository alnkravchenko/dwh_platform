from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .datasource import DatasourceModel
from .warehouse import WarehouseModel


# TODO: consider joining this 2 classes
class ProjectModel(BaseModel):
    id: Optional[UUID]
    name: str
    created_by: UUID

    class Config:
        orm_mode = True


class ProjectContent(BaseModel):
    id: UUID
    warehouse: WarehouseModel
    datasources: List[DatasourceModel]

    class Config:
        orm_mode = True
