from typing import List, Tuple
from uuid import UUID

from repos import warehouses as wh_db
from schema.user import UserModel
from schema.warehouse import WarehouseCreate, WarehouseModel, WarehouseUpdate
from sqlalchemy.orm import Session


class WarehouseService:
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.user = user

    def __add_datatables(self, wh: WarehouseModel, dts: List[UUID]):
        pass

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
        # check connection to spark cluster
        created_wh = wh_db.create_warehouse(self.db, wh)
        self.__add_datatables(created_wh, wh.datatables)
        return 200, f"Warehouse(id={created_wh.id})  created"

    def update_warehouse(
        self, wh_id: UUID, new_data: WarehouseUpdate
    ) -> Tuple[int, str]:
        new_wh = wh_db.update_warehouse(self.db, wh_id, new_data)
        if new_wh is None:
            return 400, "Bad request"
        if new_data.datatables is not None:
            self.__add_datatables(new_wh, new_data.datatables)
        return 200, f"Warehouse(id={wh_id}) updated"

    def delete_warehouse(self, wh_id: UUID) -> Tuple[int, str]:
        is_deleted = wh_db.delete_warehouse_by_id(self.db, wh_id)
        if not is_deleted:
            return 400, "Bad request"
        return 200, f"Warehouse(id={wh_id}) deleted"
