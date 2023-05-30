from typing import List
from uuid import UUID

from models.datasource import DatasourceDB
from models.project import ProjectDB
from models.user import UserDB
from models.warehouse import WarehouseDB
from schema.datasource import DatasourceModel
from schema.project import ProjectContent, ProjectCreate, ProjectModel, ProjectUpdate
from schema.user import UserModel
from schema.warehouse import WarehouseModel
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from .database import create_entity


def get_user_projects(
    db: Session, user_id: UUID, offset: int = 0, limit: int | None = 25
) -> List[ProjectModel]:
    query = (
        select(ProjectDB)
        .where(ProjectDB.created_by == user_id)
        .offset(offset)
        .limit(limit)
    )
    proj_db = db.execute(query).scalars().all()
    db.commit()
    if len(proj_db) > 0:
        return list(map(ProjectModel.from_orm, proj_db))
    return []


def get_project_by_id(db: Session, proj_id: UUID) -> ProjectModel | None:
    query = select(ProjectDB).where(ProjectDB.id == proj_id)
    proj_db = db.execute(query).scalar()
    db.commit()
    if proj_db is not None:
        return ProjectModel.from_orm(proj_db)


def get_project_by_wh_id(db: Session, wh_id: UUID) -> ProjectModel | None:
    query = (
        select(ProjectDB)
        .join(WarehouseDB, ProjectDB.id == WarehouseDB.project_id)
        .where(WarehouseDB.id == wh_id)
    )
    proj_db = db.execute(query).scalar()
    db.commit()
    if proj_db is not None:
        return ProjectModel.from_orm(proj_db)


def get_content(db: Session, user_id: UUID, project_id: UUID) -> ProjectContent | None:
    query = (
        select(ProjectDB)
        .where(ProjectDB.created_by == user_id)
        .where(ProjectDB.id == project_id)
    )
    proj_db = db.execute(query).scalar()
    # get datasources
    ds_query = select(DatasourceDB).where(DatasourceDB.project_id == project_id)
    ds_db = db.execute(ds_query).scalars().all()
    # get warehouse
    warehouse_query = select(WarehouseDB).where(WarehouseDB.project_id == project_id)
    wh_db = db.execute(warehouse_query).scalar()

    ds = []
    if ds_db is not None:
        ds = list(map(DatasourceModel.from_orm, ds_db))
    wh = None
    if wh_db is not None:
        wh = WarehouseModel.from_orm(wh_db)
    if proj_db is not None:
        return ProjectContent(id=proj_db.id, warehouse=wh, datasources=ds)  # type: ignore


def get_project_owner(db: Session, project_id: UUID) -> UserModel | None:
    query = (
        select(UserDB)
        .join(ProjectDB, UserDB.id == ProjectDB.created_by)
        .where(ProjectDB.id == project_id)
    )
    owner_db = db.execute(query).scalar()
    db.commit()
    if owner_db is not None:
        return UserModel.from_orm(owner_db)


def create_project(db: Session, proj: ProjectCreate, user_id: UUID) -> ProjectModel:
    proj_db = ProjectDB(
        name=proj.name,
        node_url=proj.node_url,
        created_by=user_id,
    )
    return ProjectModel.from_orm(create_entity(db, proj_db))


def update_project(
    db: Session, proj_id: UUID, proj: ProjectUpdate
) -> ProjectModel | None:
    new_fields = proj.dict(exclude_none=True)

    query = (
        update(ProjectDB)
        .returning(ProjectDB)
        .where(ProjectDB.id == proj_id)
        .values(**new_fields)
    )
    new_proj = db.execute(query).scalar()
    db.commit()
    if new_proj is not None:
        return ProjectModel.from_orm(new_proj)


def delete_project_by_id(db: Session, proj_id: UUID) -> bool:
    query = delete(ProjectDB).where(ProjectDB.id == proj_id)
    rows_affected = db.execute(query).rowcount  # type: ignore
    db.commit()
    return rows_affected > 0
