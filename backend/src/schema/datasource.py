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
    FILE = "file"
    DATATABLE = "datatable"


class DatasourceCreate(BaseModel):
    name: str
    project_id: UUID
    ds_type: DatasourceType
    config: Dict[str, str]

    @validator("config")
    def validate_config(cls, v: Dict[str, str]):
        keys, _ = v.items()
        host_pattern = r"^[^:/]+:\d+\/\w+$"
        if cls.ds_type == DatasourceType.FILE:
            has_filename = "filename" in keys
            if not has_filename:
                raise ValueError("Config must contain filename")
            # check file type
            is_csv = "csv" in v["filename"]
            is_json = "json" in v["filename"]
            if not is_csv and not is_json:
                raise ValueError("Only CSV and JSON files are supported")
        elif cls.ds_type == DatasourceType.DATATABLE:
            has_fields = "fields" in keys
            if not has_fields:
                raise ValueError("Config must contain table fields")

            check_fields: List[bool] = []
            for field in v["fields"]:
                parsed: Dict[str, str] = json.loads(field)
                keys = parsed.keys()
                has_name = "name" in keys
                has_type = "type" in keys
                check_fields.append(has_name and has_type)
            if not all(check_fields):
                raise ValueError(
                    "Field list must contain objects with field name and field type."
                    + 'Example: \n{"fields": [ \n{"name": "field1", "type": "int"}, '
                    + '\n{"name": "field2", "type": "str"}, '
                    + '\n{"name": "field3", "type": "double"}, '
                    + '\n{"name": "field4", "type": "bool"} \n]}'
                )
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
                raise ValueError(
                    "Config must contain host, username, password and name of tables"
                )
            # validate structure of host url
            check_host = re.match(host_pattern, v["host"]) is not None
            if not check_host:
                raise ValueError(
                    "Host must be in format <host_url>:<port>/<databaseName>"
                )

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
