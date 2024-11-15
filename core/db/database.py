# types
from sqlite3 import Connection, Cursor


class DataBase:
    def __init__(self, connection: Connection, cursor: Cursor) -> None:
        self.connection = connection
        self.cursor = cursor
