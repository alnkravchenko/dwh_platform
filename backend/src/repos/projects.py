from typing import List
from uuid import UUID

from models.project import ProjectDB
from schema.project import ProjectContent, ProjectCreate, ProjectModel, ProjectUpdate
from schema.user import UserModel
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from .database import create_entity


def get_user_projects(
    db: Session, user: UserModel, offset: int = 0, limit: int = 25
) -> List[ProjectModel]:
    query = (
        select(ProjectDB)
        .where(ProjectDB.created_by == user.id)
        .offset(offset)
        .limit(limit)
    )
    projects = db.execute(query).scalars().all()
    db.commit()
    if len(projects) > 0:
        return list(map(ProjectModel.from_orm, projects))
    return []


def get_content(db: Session, user_id: UUID, project_id: UUID) -> ProjectContent | None:
    query = (
        select(ProjectDB)
        .where(ProjectDB.created_by == user_id)
        .where(ProjectDB.id == project_id)
    )
    project_db = db.execute(query).scalar()
    if project_db is not None:
        return ProjectContent.from_orm(project_db)
    # ds_query = select(DatasourceDB).where(DatasourceDB.project_id == project_id)
    # datasources: List[DatasourceModel] = list(db.execute(ds_query).scalars().all())

    # warehouse_query = select(WarehouseDB)


def create_project(db: Session, proj: ProjectCreate) -> ProjectModel:
    proj_db = ProjectDB(name=proj.name, created_by=proj.created_by)
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
