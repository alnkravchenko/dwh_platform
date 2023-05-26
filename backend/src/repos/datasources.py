from uuid import UUID

from models.datasource import DatasourceDB
from repos.database import create_entity
from schema.datasource import DatasourceCreate, DatasourceModel, DatasourceUpdate
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session


def get_datasource_by_id(db: Session, ds_id: UUID) -> DatasourceModel | None:
    query = select(DatasourceDB).where(DatasourceDB.id == ds_id)
    ds_db = db.execute(query).scalar()
    db.commit()
    if ds_db is not None:
        return DatasourceModel.from_orm(ds_db)


def create_datasource(db: Session, ds: DatasourceCreate) -> DatasourceModel:
    ds_db = DatasourceDB(
        name=ds.name,
        project_id=ds.project_id,
        ds_type=ds.ds_type,
        config=ds.config,
    )
    return DatasourceModel.from_orm(create_entity(db, ds_db))


def update_datasource(
    db: Session, ds_id: UUID, ds: DatasourceUpdate
) -> DatasourceModel | None:
    new_fields = ds.dict(exclude_none=True)

    query = (
        update(DatasourceDB)
        .returning(DatasourceDB)
        .where(DatasourceDB.id == ds_id)
        .values(**new_fields)
    )
    new_ds_db = db.execute(query).scalar()
    db.commit()
    if new_ds_db is not None:
        return DatasourceModel.from_orm(new_ds_db)


def delete_datasource_by_id(db: Session, ds_id: UUID) -> bool:
    query = delete(DatasourceDB).where(DatasourceDB.id == ds_id)
    rows_affected = db.execute(query).rowcount  # type: ignore
    db.commit()
    return rows_affected > 0
