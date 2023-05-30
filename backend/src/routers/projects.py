from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from repos.database import get_db
from schema.project import ProjectCreate, ProjectUpdate
from schema.user import UserModel
from services.project import ProjectService
from sqlalchemy.orm import Session

from .users import get_current_user

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def get_all_projects(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    proj_service = ProjectService(db, user)
    projects = proj_service.get_user_projects()
    log.info("[GET ALL] 200")
    return JSONResponse(
        content={"details": jsonable_encoder(projects)}, status_code=200
    )


@router.get("/{project_id}")
def get_project_content(
    project_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(project_id)
    if status_code != 200:
        log.info(f"[GET CONTENT] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = proj_service.get_project_content(project_id)
    log_msg = msg
    # create response
    if status_code == 200:
        log_msg = msg.id  # type: ignore
    log.info(f"[GET CONTENT] {status_code} {log_msg}")
    return JSONResponse(
        content={"details": jsonable_encoder(msg)}, status_code=status_code
    )


@router.post("/")
def create_project(
    project: ProjectCreate,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.create_project(project)
    log.info(f"[CREATE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.put("/{project_id}")
def update_project(
    project_id: UUID,
    new_data: ProjectUpdate,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(project_id)
    if status_code != 200:
        log.info(f"[UPDATE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = proj_service.update_project(project_id, new_data)
    log.info(f"[UPDATE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.delete("/{project_id}")
def delete_project(
    project_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(project_id)
    if status_code != 200:
        log.info(f"[DELETE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = proj_service.delete_project(project_id)
    log.info(f"[DELETE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)
