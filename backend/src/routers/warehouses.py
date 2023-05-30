from uuid import UUID

import structlog
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from repos.database import get_db
from routers.users import get_current_user
from schema.user import UserModel
from schema.warehouse import WarehouseCreate, WarehouseUpdate
from services.project import ProjectService
from services.warehouse import WarehouseService
from sqlalchemy.orm import Session

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.get("/")
def get_all_warehouses(
    user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
) -> JSONResponse:
    wh_service = WarehouseService(db, user)
    warehouses = wh_service.get_user_warehouses()
    log.info("[GET ALL] 200")
    return JSONResponse(
        content={"details": jsonable_encoder(warehouses)}, status_code=200
    )


@router.get("/{wh_id}")
def get_warehouse(
    wh_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    wh_service = WarehouseService(db, user)
    status_code, msg = wh_service.validate_user_access(wh_id)
    if status_code != 200:
        log.info(f"[GET] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = wh_service.get_warehouse(wh_id)
    log_msg = msg
    # create response
    if status_code == 200:
        log_msg = msg.id  # type: ignore
    log.info(f"[GET] {status_code} {log_msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.post("/")
def create_warehouse(
    wh: WarehouseCreate,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    proj_service = ProjectService(db, user)
    status_code, msg = proj_service.validate_user_access(wh.project_id)
    if status_code != 200:
        log.info(f"[CREATE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    wh_service = WarehouseService(db, user)
    status_code, msg = wh_service.create_warehouse(wh)
    log.info(f"[CREATE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.put("/{wh_id}")
def update_warehouse(
    wh_id: UUID,
    new_data: WarehouseUpdate,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    wh_service = WarehouseService(db, user)
    status_code, msg = wh_service.validate_user_access(wh_id)
    if status_code != 200:
        log.info(f"[UPDATE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = wh_service.update_warehouse(wh_id, new_data)
    log.info(f"[UPDATE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)


@router.delete("/{wh_id}")
def delete_warehouse(
    wh_id: UUID,
    user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    wh_service = WarehouseService(db, user)
    status_code, msg = wh_service.validate_user_access(wh_id)
    if status_code != 200:
        log.info(f"[DELETE] {status_code} {msg}")
        return JSONResponse(content={"details": msg}, status_code=status_code)

    status_code, msg = wh_service.delete_warehouse(wh_id)
    log.info(f"[DELETE] {status_code} {msg}")
    return JSONResponse(content={"details": msg}, status_code=status_code)
