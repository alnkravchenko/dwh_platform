from typing import List

from schema.datatable import DataTableModel
from sqlalchemy.orm import Session


def update_tables(db: Session, tables: List[DataTableModel]) -> List[DataTableModel]:
    """
    Create or replace if exist datasource tables
    """
    return tables
