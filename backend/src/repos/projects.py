from typing import List
from uuid import UUID

from models.project import ProjectDB
from schema.project import ProjectContent, ProjectCreate, ProjectModel, ProjectUpdate
from schema.user import UserModel
from sqlalchemy import select
from sqlalchemy.orm import Session


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
