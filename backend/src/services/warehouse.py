from typing import Dict, List, Tuple
from uuid import UUID

import structlog
from repos import datatables as dt_db
from repos import warehouses as wh_db
from schema.user import UserModel
from schema.warehouse import WarehouseCreate, WarehouseModel, WarehouseUpdate
from schema.warehouseDatatable import (
    DatatableType,
    WarehouseDataTableCreate,
    WarehouseDataTableModel,
)
from services.query import QueryService
from sqlalchemy.orm import Session

log = structlog.get_logger(module=__name__)


class WarehouseService:
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.user = user

    def __parse_datatables(
        self, wh: WarehouseModel, dts: Dict[str, List[UUID]]
    ) -> List[WarehouseDataTableCreate]:
        tables: List[WarehouseDataTableCreate] = []
        wh_id = wh.id
        for dt_type, dt_ids in dts.items():
            for dt_id in dt_ids:
                table = WarehouseDataTableCreate(
                    warehouse_id=wh_id,
                    datatable_id=dt_id,
                    dt_type=DatatableType(dt_type),
                )
                tables.append(table)
        return tables

    def __add_datatables(
        self, wh: WarehouseModel, dts: Dict[str, List[UUID]]
    ) -> Tuple[bool, str | List[WarehouseDataTableModel]]:
        tables = self.__parse_datatables(wh, dts)
        # add tables to spark cluster
        query_service = QueryService(self.db, self.user)
        status, msg = query_service.add_tables(tables)
        if not status:
            return False, msg
        log.info("[DWH CREATE] Tables added to Spark cluster")
        # ingest data from the tables
        status, msg = query_service.ingest_data(tables)
        if not status:
            return False, msg
        log.info("[DWH CREATE] Data ingested to Spark cluster")
        return True, dt_db.create_warehouse_tables(self.db, tables)

    def __update_datatables(self, wh: WarehouseModel, dts: Dict[str, List[UUID]]):
        tables = self.__parse_datatables(wh, dts)
        # update in data warehouse cluster
        return dt_db.update_warehouse_tables(self.db, tables)

    def validate_user_access(self, wh_id: UUID) -> Tuple[int, str]:
        # check if warehouse exists
        wh = wh_db.get_warehouse_by_id(self.db, wh_id)
        if wh is None:
            return 404, "Not found"
        # check user access
        owner = wh_db.get_warehouse_owner(self.db, wh_id)
        if owner != self.user.id:
            return 401, "Unauthorized"
        return 200, "OK"

    def get_user_warehouses(self) -> List[WarehouseModel]:
        warehouses = wh_db.get_user_warehouses(self.db, self.user.id, limit=None)
        return warehouses

    def get_warehouse(self, wh_id: UUID) -> Tuple[int, str | WarehouseModel]:
        wh = wh_db.get_warehouse_by_id(self.db, wh_id)
        if wh is None:
            return 400, "Bad request"
        return 200, wh

    def create_warehouse(self, wh: WarehouseCreate) -> Tuple[int, str]:
        created_wh = wh_db.create_warehouse(self.db, wh)
        status, msg = self.__add_datatables(created_wh, wh.datatables)
        if not status:
            return 400, msg  # type: ignore
        return 200, f"Warehouse(id={created_wh.id}) created"

    def update_warehouse(
        self, wh_id: UUID, new_data: WarehouseUpdate
    ) -> Tuple[int, str]:
        new_wh = wh_db.update_warehouse(self.db, wh_id, new_data)
        if new_wh is None:
            return 400, "Bad request"
        if new_data.datatables is not None:
            self.__update_datatables(new_wh, new_data.datatables)
        return 200, f"Warehouse(id={wh_id}) updated, data table types changed"

    def delete_warehouse(self, wh_id: UUID) -> Tuple[int, str]:
        is_deleted = wh_db.delete_warehouse_by_id(self.db, wh_id)
        if not is_deleted:
            return 400, "Bad request"
        return 200, f"Warehouse(id={wh_id}) deleted"
