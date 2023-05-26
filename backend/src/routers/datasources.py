from typing import Dict, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse
from repos.database import get_db
from schema.datasource import DatasourceCreate, DatasourceType, DatasourceUpdate
from schema.user import UserModel
from services.datasource import DatasourceService
from services.project import ProjectService
from sqlalchemy.orm import Session

from .users import get_current_user

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/datasources", tags=["datasources"])


@router.get("/")
def get_all_datasources(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
) -> JSONResponse:
    ds_service = DatasourceService(db, user)
    datasources = ds_service.get_user_datasources()
    log.info("[GET ALL] 200")
    return JSONResponse(content={"details": datasources}, status_code=200)


@router.get("/types", response_model=Dict[str, str])
def get_datasource_types():
    return {i.name: i.value for i in DatasourceType}


@router.get("/{ds_id}")
def get_datasource(
    ds_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    ds_service = DatasourceService(db, user)
    status_code, msg = ds_service.validate_user_access(ds_id)
    if status_code != 200:
        log.info(f"[GET] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = ds_service.get_datasource_by_id(ds_id)
    # create response
    log.info(f"[GET] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.post("/")
def create_datasource(
    ds: DatasourceCreate,
    file: Optional[UploadFile],
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    # check user access
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(ds.project_id)
    if status_code != 200:
        log.info(f"[CREATE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    ds_service = DatasourceService(db, user)
    status_code, msg = ds_service.create_datasource(ds, file)
    # create response
    log.info(f"[CREATE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.put("/{ds_id}")
def update_datasource(
    ds_id: UUID,
    new_data: DatasourceUpdate,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    ds_service = DatasourceService(db, user)
    status_code, msg = ds_service.validate_user_access(ds_id)
    if status_code != 200:
        log.info(f"[UPDATE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = ds_service.update_datasource(ds_id, new_data)
    log.info(f"[UPDATE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.delete("/{ds_id}")
def delete_datasource(
    ds_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    ds_service = DatasourceService(db, user)
    status_code, msg = ds_service.validate_user_access(ds_id)
    if status_code != 200:
        log.info(f"[DELETE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = ds_service.delete_datasource(ds_id)
    log.info(f"[DELETE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.get("/{ds_id}/tables")
def get_datasource_tables(
    ds_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    ds_service = DatasourceService(db, user)
    status_code, msg = ds_service.validate_user_access(ds_id)
    if status_code != 200:
        log.info(f"[GET TABLES] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = ds_service.get_datasource_tables(ds_id)
    log.info(f"[GET TABLES] {status_code}")
    return JSONResponse(content={"details": msg}, status_code=status_code)
