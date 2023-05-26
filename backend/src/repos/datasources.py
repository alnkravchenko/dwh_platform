from typing import List
from uuid import UUID

from models.datasource import DatasourceDB
from models.project import ProjectDB
from models.user import UserDB
from repos.database import create_entity
from schema.datasource import DatasourceCreate, DatasourceModel, DatasourceUpdate
from schema.datatable import DataTableModel
from schema.user import UserModel
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session


def get_user_datasources(
    db: Session, user_id: UUID, offset: int = 0, limit: int | None = 25
) -> List[DatasourceModel]:
    query = (
        select(DatasourceDB)
        .join(ProjectDB, DatasourceDB.project_id == ProjectDB.id)
        .where(ProjectDB.created_by == user_id)
        .offset(offset)
        .limit(limit)
    )
    ds_db = db.execute(query).scalars().all()
    db.commit()
    if len(ds_db) > 0:
        return list(map(DatasourceModel.from_orm, ds_db))
    return []


def get_datasource_by_id(db: Session, ds_id: UUID) -> DatasourceModel | None:
    query = select(DatasourceDB).where(DatasourceDB.id == ds_id)
    ds_db = db.execute(query).scalar()
    db.commit()
    if ds_db is not None:
        return DatasourceModel.from_orm(ds_db)


def get_datasource_owner(db: Session, ds_id: UUID) -> UserModel | None:
    query = (
        select(UserDB)
        .join(ProjectDB, UserDB.id == ProjectDB.created_by)
        .join(DatasourceDB, ProjectDB.id == DatasourceDB.project_id)
        .where(DatasourceDB.id == ds_id)
    )
    owner_db = db.execute(query).scalar()
    db.commit()
    if owner_db is not None:
        return UserModel.from_orm(owner_db)


def create_datasource(db: Session, ds: DatasourceCreate) -> DatasourceModel:
    ds_db = DatasourceDB(
        name=ds.name,
        project_id=ds.project_id,
        ds_type=ds.ds_type,
        config=ds.config,
    )
    return DatasourceModel.from_orm(create_entity(db, ds_db))


def update_datasource(
    db: Session, ds_id: UUID, ds: DatasourceUpdate
) -> DatasourceModel | None:
    new_fields = ds.dict(exclude_none=True)

    query = (
        update(DatasourceDB)
        .returning(DatasourceDB)
        .where(DatasourceDB.id == ds_id)
        .values(**new_fields)
    )
    new_ds_db = db.execute(query).scalar()
    db.commit()
    if new_ds_db is not None:
        return DatasourceModel.from_orm(new_ds_db)


def delete_datasource_by_id(db: Session, ds_id: UUID) -> bool:
    query = delete(DatasourceDB).where(DatasourceDB.id == ds_id)
    rows_affected = db.execute(query).rowcount  # type: ignore
    db.commit()
    return rows_affected > 0


# TODO: add database func to get ds tables
def get_datasource_tables(db: Session, ds_id: UUID) -> List[DataTableModel]:
    return []
