from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, validator


class WarehouseCreate(BaseModel):
    name: str
    datatables: Dict[str, List[UUID]]
    project_id: UUID

    @validator("datatables")
    def validate_config(cls, v: Dict[str, List[UUID]]):
        keys, _ = v.items()
        if "fact" not in keys and "dimension" not in keys:
            raise ValueError(
                "Invalid data table types. Supported types are 'fact' and 'dimension'."
            )
        if keys.count("fact") > 1:
            raise ValueError(
                "Invalid amount of 'fact' type. There can be"
                + "only one fact table in data warehouse"
            )

    class Config:
        orm_mode = True


class WarehouseModel(WarehouseCreate):
    id: UUID

    class Config:
        orm_mode = True


class WarehouseUpdate(BaseModel):
    name: Optional[str]
    datatables: Optional[Dict[str, List[UUID]]]

    class Config:
        orm_mode = True
