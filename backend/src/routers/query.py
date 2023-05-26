import structlog
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse
from repos import projects as proj_db
from repos.database import get_db
from schema.query import QueryModel, QueryWrite
from schema.user import UserModel
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
    proj = proj_db.get_project_by_id(db, query.project_id)
    if proj is None:
        log.info("[QUERY] 404 Not found")
        return JSONResponse(content={"details": "Not found"}, status_code=404)
    # check user access
    if proj.created_by != user.id:
        log.info("[QUERY] 401 Unauthorized")
        return JSONResponse(content={"details": "Unauthorized"}, status_code=401)
    # validate query on master node
    query_service = QueryService(db, user)
    QueryModel.validate_query(query, query_service, logger=log, prefix="[QUERY]")
    # process query
    res = query_service.run_query(query.project_id, query.query)
    return JSONResponse(content={"details": res}, status_code=200)


@router.post("/read")
def read_data(
    query: QueryModel,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    msg = "OK"
    return JSONResponse(content={"details": msg}, status_code=200)


@router.post("/write")
def write_data(
    query: QueryWrite,
    file: UploadFile,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    msg = "OK"
    return JSONResponse(content={"details": msg}, status_code=200)
