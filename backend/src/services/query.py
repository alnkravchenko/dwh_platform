from typing import Dict, List, Tuple
from uuid import UUID

import structlog
import utils.spark_helpers as spk
from repos import datasources as ds_db
from repos import datatables as dt_db
from repos import projects as proj_db
from schema.datasource import DatasourceModel
from schema.datatable import DataTableModel
from schema.project import ProjectModel
from schema.user import UserModel
from schema.warehouseDatatable import WarehouseDataTableCreate
from sqlalchemy.orm import Session

from .project import ProjectService

log = structlog.get_logger(module=__name__)


class QueryService:
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.user = user

    def __get_node_url(self, project_id: UUID) -> str:
        proj = proj_db.get_project_by_id(self.db, project_id)
        return proj.node_url  # type: ignore

    def __group_tables_by_ds(
        self, tables: List[DataTableModel]
    ) -> Dict[UUID, List[DataTableModel]]:
        result = {}
        for table in tables:
            datasource_id = str(table.datasource_id)
            if datasource_id not in result:
                result[datasource_id] = []
            result[datasource_id].append(table)
        return result

    def __add_datasource(
        self,
        data: Dict[UUID, List[DataTableModel]],
        datasources: List[DatasourceModel],
    ) -> List[Tuple[DatasourceModel, List[DataTableModel]]]:
        result = []
        for ds in datasources:
            result.append((ds, data[str(ds.id)]))  # type: ignore
        return result

    def validate_query(self, project_id: UUID, query: str) -> Tuple[bool, str]:
        """
        Validate the syntax and validity of a PySpark query
        on node without executing it

        EFFECTS:
        * creates spark session
        """
        proj = proj_db.get_project_by_id(self.db, project_id)
        # validate user access
        status_code, msg = ProjectService(self.db, self.user).validate_user_access(
            project_id
        )
        if status_code != 200:
            return False, msg
        node_url = proj.node_url  # type: ignore
        # create spark session
        spark_session = self.__setup_connection(node_url)
        # check query
        try:
            spark_session.sql(f"EXPLAIN {query}")
            return True, "OK"
        except Exception as e:
            return False, str(e)

    def run_query(self, project_id: UUID, query: str) -> str:
        """
        Run user query

        EFFECTS:
        * creates spark session
        """
        proj = proj_db.get_project_by_id(self.db, project_id)
        node_url = proj.node_url  # type: ignore

    def add_tables(self, tables: List[WarehouseDataTableCreate]) -> Tuple[bool, str]:
        # get node_url
        proj: ProjectModel = proj_db.get_project_by_wh_id(
            self.db, tables[0].warehouse_id
        )  # type: ignore
        node_url = proj.node_url
        # select datatables
        datatables: List[DataTableModel] = [
            dt_db.get_table_by_id(self.db, wh_dt.datatable_id) for wh_dt in tables
        ]  # type: ignore
        spark_session = spk.setup_connection(node_url)
        try:
            for table in datatables:
                spk.create_table(spark_session, table.name, table.columns)  # type: ignore
            return True, "Tables created"
        except Exception as e:
            return False, str(e)
        finally:
            spark_session.stop()

    def ingest_data(self, tables: List[WarehouseDataTableCreate]) -> Tuple[bool, str]:
        """
        Ingest data from warehouse tables to spark cluster

        EFFECTS:
        * creates spark session
        """
        # get node_url
        proj: ProjectModel = proj_db.get_project_by_wh_id(
            self.db, tables[0].warehouse_id
        )  # type: ignore
        node_url = proj.node_url
        # select datatables
        datatables: List[DataTableModel] = [
            dt_db.get_table_by_id(self.db, wh_dt.datatable_id) for wh_dt in tables
        ]  # type: ignore
        # select datasources
        grouped = self.__group_tables_by_ds(datatables)
        datasources = ds_db.get_datasources_by_id(self.db, list(grouped.keys()))
        ds_grouped = self.__add_datasource(grouped, datasources)
        # run spark queries
        spark_session = spk.setup_connection(node_url)
        try:
            for ds, dstables in ds_grouped:
                spk.ingest_data(spark_session, ds, dstables)
            return True, "Data from tables ingested"
        except Exception as e:
            return False, str(e)
        finally:
            spark_session.stop()

    def read_data(self, ds: DatasourceModel, query: str) -> str:
        """
        Read data from the datasource

        EFFECTS:
        * creates spark session
        """
        # create connections regarding data source type
        return ""

    def parse_results(self, data) -> str:
        return str(data)
