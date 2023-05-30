from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from repos.database import get_db
from schema.user import UserModel
from services.datasource import DatasourceService
from sqlalchemy.orm import Session

from .users import get_current_user

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/datatables", tags=["datatables"])


@router.get("/{ds_id}")
def get_datasource_tables(
    ds_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ds_service = DatasourceService(db, user)
    status_code, msg = ds_service.validate_user_access(ds_id)
    if status_code != 200:
        log.info(f"[GET DS] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = ds_service.get_datasource_tables(ds_id)
    # create response
    log.info(f"[GET DS] {status_code} OK")
    return JSONResponse(
        content={"details": jsonable_encoder(msg)}, status_code=status_code
    )
