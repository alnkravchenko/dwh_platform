from typing import List
from uuid import UUID

from models.project import ProjectDB
from schema.project import ProjectContent
from schema.user import UserModel
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_user_projects(
    db: Session, user: UserModel, offset: int = 0, limit: int = 5
) -> List[ProjectDB]:
    query = (
        select(ProjectDB)
        .where(ProjectDB.created_by == user.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.execute(query).scalars().all())


def get_content(db: Session, project_id: UUID) -> ProjectContent:
    project_query = select(ProjectDB).where(ProjectDB.id == project_id)
    project_db = db.execute(project_query).scalar()
    return ProjectContent.from_orm(project_db)
    # ds_query = select(DatasourceDB).where(DatasourceDB.project_id == project_id)
    # datasources: List[DatasourceModel] = list(db.execute(ds_query).scalars().all())

    # warehouse_query = select(WarehouseDB)
