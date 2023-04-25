from typing import List
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
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
def get_project_content(
    project_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    content = proj_db.get_content(db, user.id, project_id)
    # create response
    status_code = 200 if content is not None else 404
    msg = content if status_code == 200 else "Not found"
    log.info(f"[GET CONTENT] {status_code} {msg}")

    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.post("/")
def create_project(
    project: ProjectCreate, db: Session = Depends(get_db)
) -> JSONResponse:
    proj_db.create_project(db, project)
    msg = "Project created"
    log.info(f"[CREATE] {200} {msg}")
    return JSONResponse(content={"details": msg}, status_code=200)


@router.put("/{project_id}")
def update_project(
    project_id: UUID, proj: ProjectUpdate, db: Session = Depends(get_db)
) -> JSONResponse:
    new_project = proj_db.update_project(db, project_id, proj)
    # create response
    status_code = 200 if new_project is not None else 404
    msg = new_project if status_code == 200 else "Not found"
    log.info(f"[UPDATE] {status_code} {msg}")

    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.delete("/{project_id}")
def delete_project(project_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    is_deleted = proj_db.delete_project_by_id(db, project_id)
    # create response
    status_code = 200 if is_deleted else 404
    msg = f"Project(id={project_id}) deleted" if status_code == 200 else "Not found"
    log.info(f"[DELETE] {status_code} {msg}")

    return JSONResponse(content={"details": msg}, status_code=status_code)
