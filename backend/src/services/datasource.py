from typing import Dict, List, Tuple
from uuid import UUID

from repos import datasources as ds_db
from repos import datatables as dt_db
from schema.datasource import (
    DatasourceCreate,
    DatasourceModel,
    DatasourceType,
    DatasourceUpdate,
)
from schema.datatable import DataTableCreate, DataTableModel
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils.databases import TableInfo, get_tables


class DatasourceService:
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.user = user

    def __parse_to_datatable(self, ds_id, table: TableInfo) -> DataTableCreate:
        table_name = table["table_name"]
        columns: List[Dict[str, str]] = table["columns"]  # type: ignore
        return DataTableCreate(name=table_name, datasource_id=ds_id, columns=columns)

    def __request_tables_from_ds(self, ds: DatasourceModel) -> List[DataTableCreate]:
        if ds.ds_type == DatasourceType.DATATABLE:
            columns: List[Dict[str, str]] = ds.config["columns"]  # type: ignore
            table = DataTableCreate(name=ds.name, datasource_id=ds.id, columns=columns)
            return [table]
        else:
            url = (
                f"{ds.ds_type.value}://"
                + f"{ds.config['username']}:{ds.config['password']}@"
                + f"{ds.config['host']}"
            )
            tables = ds.config["tables"].split(",")
            # get information about tables
            db_tables_info = get_tables(url, tables)
            # parse result
            data_tables = list(
                map(lambda e: self.__parse_to_datatable(ds.id, e), db_tables_info)
            )
            return data_tables

    def validate_user_access(self, ds_id: UUID) -> Tuple[int, str]:
        # check if datasource exists
        ds = ds_db.get_datasource_by_id(self.db, ds_id)
        if ds is None:
            return 404, "Not found"
        # check datasource owner
        ds_owner = ds_db.get_datasource_owner(self.db, ds_id)
        if ds_owner != self.user:
            return 401, "Unauthorized"
        return 200, "OK"

    def get_user_datasources(self) -> List[DatasourceModel]:
        datasources = ds_db.get_user_datasources(self.db, self.user.id, limit=None)
        return datasources

    def get_datasource_by_id(self, ds_id: UUID) -> Tuple[int, str | DatasourceModel]:
        ds = ds_db.get_datasource_by_id(self.db, ds_id)
        if ds is None:
            return 400, "Bad request"
        return 200, ds

    def get_datasource_tables(self, ds_id: UUID) -> Tuple[int, List[DataTableModel]]:
        tables = dt_db.get_datasource_tables(self.db, ds_id)
        return 200, tables

    def create_datasource(self, ds: DatasourceCreate) -> Tuple[int, str]:
        ds = ds_db.create_datasource(self.db, ds)
        # create tables in database
        tables = self.__request_tables_from_ds(ds)
        dt_db.create_tables(self.db, tables)
        return 200, f"Datasource(id={ds.id}) created, tables added"

    def update_datasource(
        self, ds_id: UUID, new_data: DatasourceUpdate
    ) -> Tuple[int, str]:
        new_ds = ds_db.update_datasource(self.db, ds_id, new_data)
        if new_ds is None:
            return 400, "Bad request"
        # add or update datasource tables into database
        tables = self.__request_tables_from_ds(new_ds)
        dt_db.update_tables(self.db, tables)
        return 200, f"Datasource(id={ds_id}) columns updated"

    def delete_datasource(self, ds_id: UUID) -> Tuple[int, str]:
        is_deleted = ds_db.delete_datasource_by_id(self.db, ds_id)
        if not is_deleted:
            return 400, "Bad request"
        return 200, f"Datasource(id={ds_id}) deleted"
