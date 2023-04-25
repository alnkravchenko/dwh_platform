from __future__ import annotations

from enum import Enum
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class DatasourceType(Enum):
    mysql = 1
    postgresql = 2
    mongodb = 3
    file = 4
    api = 5


# TODO: add config JSON validation that depends on ds_type
class DatasourceCreate(BaseModel):
    name: str
    project_id: UUID
    ds_type: DatasourceType
    config: Dict[str, str]

    class Config:
        orm_mode = True


class DatasourceModel(DatasourceCreate):
    id: UUID

    class Config:
        orm_mode = True


class DatasourceUpdate(BaseModel):
    name: Optional[str]
    project_id: Optional[UUID]
    ds_type: Optional[DatasourceType]
    config: Optional[Dict[str, str]]

    class Config:
        orm_mode = True
