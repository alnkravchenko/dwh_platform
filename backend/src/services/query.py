from typing import Tuple
from uuid import UUID

from delta.pip_utils import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from repos import projects as proj_db
from schema.datasource import DatasourceModel
from schema.user import UserModel
from sqlalchemy.orm import Session

from .project import ProjectService


class QueryService:
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.user = user

    def __setup_connection(self, url: str) -> SparkSession:
        session_build = (
            SparkSession.builder.remote(url)  # type: ignore
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config(
                "spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            )
        )
        spark = configure_spark_with_delta_pip(session_build).getOrCreate()
        return spark

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

        spark_session = self.__setup_connection(node_url)
        try:
            res = spark_session.sql(query).toJSON()
            return res  # type: ignore
        except Exception as e:
            return str(e)

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
