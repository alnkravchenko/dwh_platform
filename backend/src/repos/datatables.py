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


def get_table_by_id(db: Session, dt_id: UUID) -> DataTableModel | None:
    query = select(DataTableDB).where(DataTableDB.id == dt_id)
    dt_db = db.execute(query).scalar()
    db.commit()
    if dt_db is not None:
        return DataTableModel.from_orm(dt_db)


def create_tables(db: Session, tables: List[DataTableCreate]) -> List[DataTableModel]:
    ds_id = tables[0].datasource_id
    created_tables: List[DataTableDB] = []
    for table in tables:
        # create a new table
        dt_db = DataTableDB(name=table.name, datasource_id=ds_id, columns=table.columns)
        # add the new table to the list
        db.add(dt_db)
        created_tables.append(dt_db)
    # commit the changes to the database
    db.commit()
    return list(map(DataTableModel.from_orm, created_tables))


def update_tables(db: Session, tables: List[DataTableCreate]) -> List[DataTableModel]:
    """
    Create or replace if datasource tables exist
    """
    ds_id = tables[0].datasource_id
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
                .values(columns=table.columns)
            )
            # add the updated table to the list
            updated_tables.append(dt_db)
        else:
            # create a new table
            new_dt = DataTableDB(
                name=table.name, datasource_id=ds_id, columns=table.columns
            )
            # add the new table to the list
            db.add(new_dt)
            updated_tables.append(new_dt)
    # commit the changes to the database
    db.commit()
    return list(map(DataTableModel.from_orm, updated_tables))


def create_warehouse_tables(
    db: Session, tables: List[WarehouseDataTableCreate]
) -> List[WarehouseDataTableModel]:
    wh_id = tables[0].warehouse_id
    created_tables: List[WarehouseDataTableDB] = []
    for table in tables:
        # create a new table
        whdt_db = WarehouseDataTableDB(
            warehouse_id=wh_id,
            datatable_id=table.datatable_id,
            dt_type=table.dt_type,
        )
        # add the new table to the list
        db.add(whdt_db)
        created_tables.append(whdt_db)
    # commit the changes to the database
    db.commit()
    return list(map(WarehouseDataTableModel.from_orm, created_tables))


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
            continue
            # # update the existing table with the new data
            # whdt_db = db.execute(
            #     update(WarehouseDataTableDB)
            #     .returning(WarehouseDataTableDB)
            #     .where(WarehouseDataTableDB.warehouse_id == wh_id)
            #     .where(WarehouseDataTableDB.datatable_id == table.datatable_id)
            #     .values(dt_type=table.dt_type)
            # )
            # # add the updated table to the list
            # updated_tables.append(whdt_db)
        # create a new table
        new_whdt = WarehouseDataTableDB(
            warehouse_id=wh_id,
            datatable_id=table.datatable_id,
            dt_type=table.dt_type,
        )
        # add the new table to the list
        db.add(new_whdt)
        updated_tables.append(new_whdt)
    # commit the changes to the database
    db.commit()
    return list(map(WarehouseDataTableModel.from_orm, updated_tables))
