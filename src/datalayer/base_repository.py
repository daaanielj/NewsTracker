# src/datalayer/base_repository.py
import pyodbc


# TODO: Refactor the repositories to extend this baserepository instead
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
            f"SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
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
