import os
import uuid
from typing import Dict, List, Tuple, TypedDict
from urllib.parse import urlparse

import mysql.connector
import psycopg2
from pymongo import MongoClient


class ColumnInfo(TypedDict):
    name: str
    type: str


class TableInfo(TypedDict):
    table_name: str
    columns: List[ColumnInfo]


def create_postgres_connection(url: str):
    return psycopg2.connect(url)


def parse_mysql_url(url: str) -> Dict[str, str]:
    parsed_url = urlparse(url)
    username = parsed_url.username
    password = parsed_url.password
    hostname = parsed_url.hostname
    port = parsed_url.port
    database = parsed_url.path.strip("/")

    connection_dict = {
        "user": username,
        "password": password,
        "host": hostname,
        "port": port,
        "database": database,
    }
    return connection_dict


def create_mysql_connection(url: str):
    return mysql.connector.connect(**parse_mysql_url(url))


def parse_mongodb_url(url: str) -> Tuple[str, str]:
    db_name = url.split("/")[-1]
    url = url.split(db_name)[0][:-1]
    return url, db_name


def create_mongodb_connection(url: str):
    url, db_name = parse_mongodb_url(url)
    # establish connection
    client = MongoClient(url)
    return client, db_name


def parse_data_type_mongodb(data_type: str) -> str:
    mapping = {
        "int": "int",
        "long": "int",
        "double": "float",
        "float": "float",
        "decimal": "float",
        "string": "str",
    }
    return mapping[data_type.lower()]


def parse_data_type_mysql(data_type: str) -> str:
    data_type = data_type.split("(")[0]
    mapping = {
        "int": "int",
        "tinyint": "int",
        "smallint": "int",
        "mediumint": "int",
        "bigint": "int",
        "float": "float",
        "double": "float",
        "decimal": "float",
        "char": "str",
        "varchar": "str",
        "text": "str",
    }
    return mapping[data_type.lower()]


def parse_data_type_postgres(data_type: str) -> str:
    mapping = {
        "integer": "int",
        "bigint": "int",
        "smallint": "int",
        "decimal": "float",
        "numeric": "float",
        "real": "float",
        "double precision": "float",
        "character": "str",
        "character varying": "str",
        "text": "str",
    }
    return mapping[data_type.lower()]


def get_postgres_tables(url: str) -> List[str]:
    conn = create_postgres_connection(url)
    # establish connection
    cursor = conn.cursor()
    cursor.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    )
    tables = cursor.fetchall()
    # close connection
    cursor.close()
    conn.close()
    return [table[0] for table in tables]


def get_postgres_tables_info(
    url: str, tables: List[str]
) -> List[Dict[str, str | List[Dict[str, str]]]]:
    table_info = []
    # establish connection
    conn = create_postgres_connection(url)
    cursor = conn.cursor()
    for table_name in tables:
        cursor.execute(
            f"""
            SELECT column_name, data_type FROM information_schema.columns
            WHERE table_name = '{table_name}';
            """
        )
        columns = cursor.fetchall()
        column_info = [
            {"name": column[0], "type": parse_data_type_postgres(column[1])}
            for column in columns
        ]
        table_info.append({"table_name": table_name, "columns": column_info})
    # close connection
    cursor.close()
    conn.close()
    return table_info


def get_mysql_tables(url: str) -> List[str]:
    # establish connection
    conn = create_mysql_connection(url)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    # close connection
    cursor.close()
    conn.close()
    return [table for table in tables]  # type: ignore


def get_mysql_tables_info(url: str, tables: List[str]):
    table_info = []
    # establish connection
    conn = create_mysql_connection(url)
    cursor = conn.cursor()
    for table in tables:
        cursor.execute(f"SHOW COLUMNS FROM {table};")
        columns = cursor.fetchall()
        # parse results
        column_info = [
            {
                "name": column[0],
                "type": parse_data_type_mysql(column[1].decode("utf-8")),  # type: ignore
            }
            for column in columns
        ]
        table_info.append({"table_name": table, "columns": column_info})
    # close connection
    cursor.close()
    conn.close()
    return table_info


def get_mongodb_tables(url: str):
    # establish connection
    client, db_name = create_mongodb_connection(url)
    db = client[db_name]
    tables = db.list_collection_names()
    # close connection
    client.close()
    return tables


def get_mongodb_tables_info(url: str, colls: List[str]):
    table_info = []
    # establish connection
    client, db_name = create_mongodb_connection(url)
    db = client[db_name]
    for collection_name in colls:
        collection = db[collection_name]
        columns = collection.find_one()
        # parse results
        column_info = []
        for key, value in columns.items():  # type: ignore
            if key == "_id":
                continue
            column_info.append({"name": key, "type": type(value).__name__})
        table_info.append({"table_name": collection_name, "columns": column_info})
    # close connection
    client.close()
    return table_info


def get_tables(database_url: str, tables: List[str]) -> List[TableInfo]:
    database_functions = {
        "postgres://": (get_postgres_tables, get_postgres_tables_info),
        "postgresql://": (get_postgres_tables, get_postgres_tables_info),
        "mysql://": (get_mysql_tables, get_mysql_tables_info),
        "mongodb://": (get_mongodb_tables, get_mongodb_tables_info),
    }

    for prefix, (get_tables, get_tables_info) in database_functions.items():
        if database_url.startswith(prefix):
            # tables = get_tables(database_url)
            tables_info = get_tables_info(database_url, tables)
            return tables_info

    raise ValueError("Unsupported database URL")


def read_from_postgres(url: str, table_name: str):
    conn = create_postgres_connection(url)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    # Write data to a file
    filepath = os.path.join("tmp", f"{uuid.uuid4().hex}.csv")
    with open(filepath, "w") as file:
        for row in data:
            file.write(",".join(map(str, row)) + "\n")
    cursor.close()
    conn.close()
    return filepath


def read_from_mysql(url: str, table_name: str):
    conn = create_mysql_connection(url)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    # Write data to a file
    filepath = os.path.join("tmp", f"{uuid.uuid4().hex}.csv")
    with open(filepath, "w") as file:
        for row in data:
            file.write(",".join(map(str, row)) + "\n")
    cursor.close()
    conn.close()
    return filepath


def read_from_mongodb(url: str, table_name: str) -> str:
    client, db_name = create_mongodb_connection(url)
    db = client[db_name]
    collection = db[table_name]
    data = collection.find()
    # Write data to a file
    filepath = os.path.join("tmp", f"{uuid.uuid4().hex}.json")
    with open(filepath, "w") as file:
        for document in data:
            file.write(str(document) + "\n")
    client.close()
    return filepath


def read_from_db(url: str, table_name: str) -> str:
    database_functions = {
        "postgres://": read_from_postgres,
        "postgresql://": read_from_postgres,
        "mysql://": read_from_mysql,
        "mongodb://": read_from_mongodb,
    }
    for prefix, read_from in database_functions.items():
        if url.startswith(prefix):
            file_path = read_from(url, table_name)
            return file_path

    raise ValueError("Unsupported database URL")
