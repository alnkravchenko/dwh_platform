from typing import List
from uuid import UUID

from models.project import ProjectDB
from models.user import UserDB
from models.warehouse import WarehouseDB
from schema.user import UserModel
from schema.warehouse import WarehouseCreate, WarehouseModel, WarehouseUpdate
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from .database import create_entity


def get_user_warehouses(
    db: Session, user_id: UUID, offset: int = 0, limit: int | None = 25
) -> List[WarehouseModel]:
    query = (
        select(WarehouseDB)
        .join(ProjectDB, WarehouseDB.project_id == ProjectDB.id)
        .where(ProjectDB.created_by == user_id)
        .offset(offset)
        .limit(limit)
    )
    wh_db = db.execute(query).scalars().all()
    db.commit()
    if len(wh_db) > 0:
        return list(map(WarehouseModel.from_orm, wh_db))
    return []


def get_warehouse_by_id(db: Session, wh_id: UUID) -> WarehouseModel:
    query = select(WarehouseDB).where(WarehouseDB.id == wh_id)
    wh_db = db.execute(query).scalar()
    return WarehouseModel.from_orm(wh_db)


def get_warehouse_owner(db: Session, wh_id: UUID) -> UserModel | None:
    query = (
        select(UserDB)
        .join(ProjectDB, UserDB.id == ProjectDB.created_by)
        .join(WarehouseDB, ProjectDB.id == WarehouseDB.project_id)
        .where(WarehouseDB.id == wh_id)
    )
    owner_db = db.execute(query).scalar()
    db.commit()
    if owner_db is not None:
        return UserModel.from_orm(owner_db)


def create_warehouse(db: Session, wh: WarehouseCreate) -> WarehouseModel:
    wh_db = WarehouseDB(name=wh.name, project_id=wh.project_id)
    return WarehouseModel.from_orm(create_entity(db, wh_db))


def update_warehouse(
    db: Session, wh_id: UUID, wh: WarehouseUpdate
) -> WarehouseModel | None:
    new_fields = wh.dict(exclude_none=True)

    query = (
        update(WarehouseDB)
        .returning(WarehouseDB)
        .where(WarehouseDB.id == wh_id)
        .values(**new_fields)
    )
    new_wh_db = db.execute(query).scalar()
    db.commit()
    if new_wh_db is not None:
        return WarehouseModel.from_orm(new_wh_db)


def delete_warehouse_by_id(db: Session, wh_id: UUID) -> bool:
    query = delete(WarehouseDB).where(WarehouseDB.id == wh_id)
    rows_affected = db.execute(query).rowcount  # type: ignore
    db.commit()
    return rows_affected > 0
