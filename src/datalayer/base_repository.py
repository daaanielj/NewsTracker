# src/datalayer/base_repository.py
import pyodbc


class BaseRepository:
    def __init__(self, server: str, database: str, username: str, password: str):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = self._connect()

    def _connect(self):
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password}"
        )
        return pyodbc.connect(connection_string)

    def execute_query(self, query: str, params: tuple = ()):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()
            return cursor

    def fetch_all(self, query: str, params: tuple = ()):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()
