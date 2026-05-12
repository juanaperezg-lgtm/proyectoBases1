from contextlib import contextmanager

import mysql.connector
from mysql.connector import MySQLConnection

from app.config import DB_CONFIG


@contextmanager
def get_connection(use_database: bool = True):
    config = dict(DB_CONFIG)
    if not use_database:
        config.pop("database", None)
    connection: MySQLConnection = mysql.connector.connect(**config)
    try:
        yield connection
    finally:
        connection.close()


def run_statements(statements: list[str], use_database: bool = True) -> None:
    with get_connection(use_database=use_database) as conn:
        cursor = conn.cursor()
        try:
            for statement in statements:
                cursor.execute(statement)
            conn.commit()
        finally:
            cursor.close()
