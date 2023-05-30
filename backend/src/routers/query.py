from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from repos.database import get_db
from schema.query import QueryModel
from schema.user import UserModel
from services.project import ProjectService
from services.query import QueryService
from sqlalchemy.orm import Session

from .users import get_current_user

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/query", tags=["query"])


@router.post("/")
def run_query(
    query: QueryModel,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(query.project_id)
    if status_code != 200:
        log.info(f"[RUN QUERY] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)
    # validate query on master node
    query_service = QueryService(db, user)
    status_code, msg = query_service.validate_query(query.project_id, query.query)
    if status_code != 200:
        log.info(f"[RUN QUERY] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)
    # process query
    status, msg = query_service.run_query(query.project_id, query.query)
    if not status:
        log.info(f"[RUN QUERY] 400 {msg}")
        return JSONResponse(content={"details": msg}, status_code=400)
    log.info("[RUN QUERY] 200 OK")
    return JSONResponse(content={"details": jsonable_encoder(msg)}, status_code=200)


@router.post("/read")
def read_data(
    query: QueryModel,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(query.project_id)
    if status_code != 200:
        log.info(f"[READ] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)
    # validate query on master node
    query_service = QueryService(db, user)
    status_code, msg = query_service.validate_query(query.project_id, query.query)
    if status_code != 200:
        log.info(f"[RUN QUERY] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)
    # process query
    status_code, msg = query_service.read_data(query.project_id, query.query)
    log.info(f"[RUN QUERY] {status_code} {msg}")
    if status_code != 200:
        return JSONResponse(content={"details": msg}, status_code=400)

    return JSONResponse(content={"details": jsonable_encoder(msg)}, status_code=200)


@router.post("/write")
def write_data(
    project_id: UUID = Form(),
    datatable_id: UUID = Form(),
    user_file: UploadFile | None = None,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(project_id)
    if status_code != 200:
        log.info(f"[WRITE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)
    query_service = QueryService(db, user)
    if user_file is not None:
        status_code, msg = query_service.validate_file(user_file)
        if status_code != 200:
            log.info(f"[WRITE] {status_code} {msg}")
            return JSONResponse(content={"details": msg}, status_code=status_code)
    # process query
    status_code, msg = query_service.write_data(project_id, datatable_id, user_file)
    log.info(f"[WRITE] {status_code} {msg}")

    if status_code != 200:
        return JSONResponse(content={"details": msg}, status_code=400)
    return JSONResponse(content={"details": msg}, status_code=200)
