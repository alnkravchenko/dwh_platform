from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from repos import projects as proj_db
from repos.database import get_db
from schema.user import UserModel
from sqlalchemy.orm import Session

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def get_all_projects(
    user: UserModel, offset: int = 0, limit: int = 5, db: Session = Depends(get_db)
):
    return proj_db.get_user_projects(db, user, offset, limit)


@router.get("/{project_id}")
def get_project_content(project_id: UUID, db: Session = Depends(get_db)):
    return proj_db.get_content(db, project_id)
