from typing import List
from uuid import UUID

from models.datatable import DataTableDB
from models.warehouseDatatable import WarehouseDataTableDB
from schema.datatable import DataTableCreate, DataTableModel
from schema.warehouseDatatable import WarehouseDataTableCreate, WarehouseDataTableModel
from sqlalchemy import select, update
from sqlalchemy.orm import Session


def get_datasource_tables(
    db: Session, ds_id: UUID, offset: int = 0, limit: int | None = 25
) -> List[DataTableModel]:
    query = (
        select(DataTableDB)
        .where(DataTableDB.datasource_id == ds_id)
        .offset(offset)
        .limit(limit)
    )
    dt_db = db.execute(query).scalars().all()
    db.commit()
    if len(dt_db) > 0:
        return list(map(DataTableModel.from_orm, dt_db))
    return []


def create_tables(db: Session, tables: List[DataTableCreate]) -> List[DataTableModel]:
    ds_id = tables[0].ds_id
    created_tables: List[DataTableModel] = []
    for table in tables:
        # create a new table
        dt_db = DataTableDB(name=table.name, datasource_id=ds_id, fields=table.fields)
        # add the new table to the list
        db.add(dt_db)
        created_tables.append(DataTableModel.from_orm(dt_db))
    # commit the changes to the database
    db.commit()
    return created_tables


def update_tables(db: Session, tables: List[DataTableCreate]) -> List[DataTableModel]:
    """
    Create or replace if datasource tables exist
    """
    ds_id = tables[0].ds_id
    updated_tables = []
    # get the list of existing table names
    existing_table_names = [
        name
        for name in db.execute(
            select(DataTableDB.name).where(DataTableDB.datasource_id == ds_id)
        )
    ]
    for table in tables:
        if table.name in existing_table_names:
            # update the existing table with the new data
            dt_db = db.execute(
                update(DataTableDB)
                .returning(DataTableDB)
                .where(DataTableDB.datasource_id == ds_id)
                .where(DataTableDB.name == table.name)
                .values(fields=table.fields)
            )
            # add the updated table to the list
            updated_dt = DataTableModel.from_orm(dt_db)
            updated_tables.append(updated_dt)
        else:
            # create a new table
            new_dt = DataTableDB(
                name=table.name, datasource_id=ds_id, fields=table.fields
            )
            # add the new table to the list
            db.add(new_dt)
            updated_tables.append(DataTableModel.from_orm(new_dt))
    # commit the changes to the database
    db.commit()
    return updated_tables


def create_warehouse_tables(
    db: Session, tables: List[WarehouseDataTableCreate]
) -> List[WarehouseDataTableModel]:
    wh_id = tables[0].warehouse_id
    created_tables: List[WarehouseDataTableModel] = []
    for table in tables:
        # create a new table
        whdt_db = WarehouseDataTableDB(
            warehouse_id=wh_id,
            datatable_id=table.datatable_id,
            dt_type=table.dt_type,
        )
        # add the new table to the list
        db.add(whdt_db)
        created_tables.append(WarehouseDataTableModel.from_orm(whdt_db))
    # commit the changes to the database
    db.commit()
    return created_tables


def update_warehouse_tables(
    db: Session, tables: List[WarehouseDataTableCreate]
) -> List[WarehouseDataTableModel]:
    """
    Create or replace if warehouse tables exist
    """
    wh_id = tables[0].warehouse_id
    updated_tables = []
    # get the list of existing datatable IDs
    existing_datatables_ids = [
        dt_id
        for dt_id in db.execute(
            select(WarehouseDataTableDB.datatable_id).where(
                WarehouseDataTableDB.warehouse_id == wh_id
            )
        )
    ]
    for table in tables:
        if table.datatable_id in existing_datatables_ids:
            # update the existing table with the new data
            whdt_db = db.execute(
                update(WarehouseDataTableDB)
                .returning(WarehouseDataTableDB)
                .where(WarehouseDataTableDB.warehouse_id == wh_id)
                .where(WarehouseDataTableDB.datatable_id == table.datatable_id)
                .values(dt_type=table.dt_type)
            )
            # add the updated table to the list
            updated_whdt = WarehouseDataTableModel.from_orm(whdt_db)
            updated_tables.append(updated_whdt)
        else:
            # create a new table
            new_whdt = WarehouseDataTableDB(
                warehouse_id=wh_id,
                datatable_id=table.datatable_id,
                dt_type=table.dt_type,
            )
            # add the new table to the list
            db.add(new_whdt)
            updated_tables.append(WarehouseDataTableModel.from_orm(new_whdt))
    # commit the changes to the database
    db.commit()
    return updated_tables
