from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import UploadFile
from repos import datasources as ds_db
from repos import datatables as dt_db
from schema.datasource import DatasourceCreate, DatasourceModel, DatasourceUpdate
from schema.datatable import DataTableModel
from schema.user import UserModel
from services.query import QueryService
from sqlalchemy.orm import Session


class DatasourceService:
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.user = user

    def __parse_tables(self, tables: List[str]) -> List[DataTableModel]:
        res: List[DataTableModel] = []
        return res

    # TODO: write a request to datasource and parse all tables with fields
    def __request_tables_from_ds(self, ds: DatasourceModel) -> List[DataTableModel]:
        query_service = QueryService(self.db, self.user)
        data_tables: List[DataTableModel] = []
        if ds.ds_type.value == "postgres":
            database_name = ds.config["host"].split("/")[-1]
            res = query_service.run_query(
                ds.project_id,
                "SELECT * FROM information_schema.tables"
                + f"WHERE table_schema = '{database_name}'",
            )
            tables = res.split(",")
            data_tables = self.__parse_tables(tables)
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
        tables = ds_db.get_datasource_tables(self.db, ds_id)
        return 200, tables

    def create_datasource(
        self, ds: DatasourceCreate, user_file: Optional[UploadFile] = None
    ) -> Tuple[int, str]:
        ds = ds_db.create_datasource(self.db, ds)
        # create datasource tables in data warehouse
        tables = self.__request_tables_from_ds(ds)
        # update or create tables in database
        dt_db.update_tables(self.db, tables)
        # fill tables with data
        if user_file is not None:
            user_file.file.read()
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
        return 200, f"Datasource(id={ds_id}) updated"

    def delete_datasource(self, ds_id: UUID) -> Tuple[int, str]:
        is_deleted = ds_db.delete_datasource_by_id(self.db, ds_id)
        if not is_deleted:
            return 400, "Bad request"
        return 200, f"Datasource(id={ds_id}) deleted"
