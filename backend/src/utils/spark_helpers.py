import os
from typing import List

import pandas as pd
from delta.pip_utils import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DataType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)
from schema.datasource import DatasourceModel
from schema.datatable import DataTableModel
from utils.databases import ColumnInfo


def setup_connection(url: str) -> SparkSession:  # type: ignore
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


def run_query(spark: SparkSession, query: str) -> List[str]:
    return spark.sql(query).toJSON().collect()


def create_schema(columns: List[db_utils.ColumnInfo]) -> StructType:
    schema = StructType(
        [
            StructField(
                column["name"],
                get_column_type(column["type"]),
                nullable=True,
            )
            for column in columns
        ]
    )
    return schema


def create_table(
    spark: SparkSession, table_name: str, columns: List[db_utils.ColumnInfo]
):
    schema = create_schema(columns)
    df = spark.createDataFrame([], schema)
    df.write.format("delta").mode("overwrite").saveAsTable(table_name)


def get_column_type(column_type: str) -> DataType:
    """
    Map column type string to corresponding PySpark data type
    """
    if column_type == "int":
        return IntegerType()
    if column_type == "str":
        return StringType()
    if column_type == "float":
        return FloatType()
    return StringType()


def ingest_data(spark: SparkSession, ds: DatasourceModel, tables: List[DataTableModel]):
    ds_url = (
        f"{ds.ds_type.value}://"
        + f"{ds.config['username']}:{ds.config['password']}@"
        + f"{ds.config['host']}"
    )
    for table in tables:
        # get data into file
        columns = [item["name"] for item in table.columns]
        schema = create_schema(table.columns)  # type: ignore
        filepath = db_utils.read_from_db(ds_url, columns, table.name)
        # ingest data
        file_format = filepath.split(".")[-1]
        if file_format.lower() == "json":
            df = pd.read_json(filepath)
        else:
            df = pd.read_csv(filepath)
        df_spark = spark.createDataFrame(df, schema)
        df_spark.write.format("delta").mode("append").saveAsTable(table.name)
        # delete file
        os.unlink(filepath)
