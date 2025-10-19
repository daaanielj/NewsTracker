import pyodbc


class Database:
    """Centralized database connection manager."""

    def __init__(self, server: str, database: str, username: str, password: str):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self._connection = None

    def connect(self):
        if self._connection is None:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
            )
            self._connection = pyodbc.connect(conn_str)
        return self._connection

    @property
    def connection(self):
        return self.connect()
