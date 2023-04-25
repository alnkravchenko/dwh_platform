from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from repos import datasources as ds_db
from repos.database import get_db
from schema.datasource import DatasourceCreate, DatasourceUpdate
from sqlalchemy.orm import Session

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/datasources", tags=["datasources"])


# TODO: add user verification by token
@router.get("/{ds_id}")
def get_datasource(ds_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    ds = ds_db.get_datasource_by_id(db, ds_id)
    # create response
    status_code = 200 if ds is not None else 404
    msg = ds if status_code == 200 else "Not found"
    log.info(f"[GET] {status_code} {msg}")

    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.post("/")
def create_datasource(
    ds: DatasourceCreate, db: Session = Depends(get_db)
) -> JSONResponse:
    ds_db.create_datasource(db, ds)
    msg = "Datasource created"
    log.info(f"[CREATE] {200} {msg}")
    return JSONResponse(content={"details": msg}, status_code=200)


@router.put("/{ds_id}")
def update_datasource(
    ds_id: UUID, ds: DatasourceUpdate, db: Session = Depends(get_db)
) -> JSONResponse:
    new_ds = ds_db.update_datasource(db, ds_id, ds)
    # create response
    status_code = 200 if new_ds is not None else 404
    msg = new_ds if status_code == 200 else "Not found"
    log.info(f"[UPDATE] {status_code} {msg}")

    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.delete("/{ds_id}")
def delete_datasource(ds_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    is_deleted = ds_db.delete_datasource_by_id(db, ds_id)
    # create response
    status_code = 200 if is_deleted else 404
    msg = f"Datasource(id={ds_id}) deleted" if status_code == 200 else "Not found"
    log.info(f"[DELETE] {status_code} {msg}")

    return JSONResponse(content={"details": msg}, status_code=status_code)
