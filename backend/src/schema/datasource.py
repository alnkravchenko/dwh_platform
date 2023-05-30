import json
import re
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, validator


class DatasourceType(str, Enum):
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    DATATABLE = "datatable"


class DatasourceCreate(BaseModel):
    name: str
    project_id: UUID
    ds_type: DatasourceType
    config: Dict[str, str]

    @validator("config")
    def validate_config(cls, v: Dict[str, str], values):
        ds_type = DatasourceType(values["ds_type"])
        keys = v.keys()
        host_pattern = r"^[^:/]+:\d+\/\w+$"
        if ds_type == DatasourceType.DATATABLE:
            has_fields = "columns" in keys
            if not has_fields:
                msg = "Config must contain table column names"
                raise ValueError(msg)
            check_fields: List[bool] = []
            for field in v["columns"]:
                parsed: Dict[str, str] = json.loads(field)
                keys = parsed.keys()
                has_name = "name" in keys
                has_type = "type" in keys
                check_fields.append(has_name and has_type)
            if not all(check_fields):
                msg = (
                    "Field list must contain objects with field name and field type."
                    + 'Example: \n{"columns": [ \n{"name": "col1", "type": "int"}, '
                    + '\n{"name": "col2", "type": "str"}, '
                    + '\n{"name": "col3", "type": "double"}, '
                    + '\n{"name": "col4", "type": "bool"} \n]}'
                )
                raise ValueError(msg)
        else:
            has_host = "host" in keys
            has_username = "username" in keys
            has_password = "password" in keys
            has_table_names = "tables" in keys
            if (
                not has_host
                or not has_username
                or not has_password
                or not has_table_names
            ):
                msg = "Config must contain host, username, password and name of tables"
                raise ValueError(msg)
            # validate structure of host url
            check_host = re.match(host_pattern, v["host"]) is not None
            if not check_host:
                msg = "Host must be in format <host_url>:<port>/<databaseName>"
                raise ValueError(msg)
        return v

    class Config:
        orm_mode = True


class DatasourceModel(DatasourceCreate):
    id: UUID

    class Config:
        orm_mode = True


class DatasourceUpdate(BaseModel):
    name: Optional[str]
    ds_type: Optional[DatasourceType]
    config: Optional[Dict[str, str]]

    class Config:
        orm_mode = True
