from typing import List
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from repos import projects as proj_db
from repos.database import get_db
from schema.project import ProjectCreate, ProjectModel, ProjectUpdate
from schema.user import UserModel
from sqlalchemy.orm import Session

from .users import get_current_user

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/projects", tags=["projects"])


# TODO: add user verification by token
@router.get("/", response_model=List[ProjectModel])
def get_all_projects(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    if user is not None:
        projects = proj_db.get_user_projects(db, user)
        log.info(f"[GET ALL BY USER] {projects}")
        return projects


@router.get("/{project_id}")
def get_project_content(project_id: UUID, db: Session = Depends(get_db)):
    return proj_db.get_content(db, project_id)
