# types
from web3.types import HexBytes
from sqlite3 import Connection, Cursor

# core
from core.models.value import Value
from core.db.database import DataBase
from core.models.command import Command
from core.models.session import Session


_ = Value('')
_ = Command('')
_ = HexBytes('')


class TableSessions(DataBase):
    NAME = 'sessions'
    KEY_INDEX = '"index"'
    KEY_COMMANDS = '"commands"'

    def __init__(self, connection: Connection, cursor: Cursor):
        super().__init__(connection, cursor)
        self._initialize_table()

    def _initialize_table(self) -> None:
        headers = f'(' \
                  f'{self.KEY_INDEX} INTEGER PRIMARY KEY,' \
                  f'{self.KEY_COMMANDS} TEXT' \
                  f')'
        self.connection.execute(f'CREATE TABLE IF NOT EXISTS {self.NAME} {headers}')
        self.connection.commit()

    def clear_database(self, ) -> None:
        self.connection.execute(f'DROP TABLE IF EXISTS {self.NAME}')
        self._initialize_table()
        self.connection.commit()

    def add_session(self, session: Session) -> None:
        self.cursor.execute('INSERT INTO ' + self.NAME + ' VALUES (?, ?)', (session.index, str(session.commands)))
        self.connection.commit()

    def delete_session(self, session: Session) -> None:
        self.cursor.execute(f'DELETE FROM {self.NAME} WHERE {self.KEY_INDEX} = ?', (session.index,))
        self.connection.commit()

    def delete_session_by_index(self, index: int) -> None:
        self.cursor.execute(f'DELETE FROM {self.NAME} WHERE {self.KEY_INDEX} = ?', (index,))
        self.connection.commit()

    def change_session(self, session: Session) -> None:
        self.cursor.execute(f'UPDATE {self.NAME} SET {self.KEY_COMMANDS} = ? WHERE {self.KEY_INDEX} = ?', (str(session.commands), session.index))
        self.connection.commit()

    def get_session(self, index: int) -> Session:
        self.cursor.execute(f'SELECT {self.KEY_COMMANDS} FROM {self.NAME} WHERE {self.KEY_INDEX} = ?', (index,))
        return Session(index=index, commands=eval(self.cursor.fetchone()[0]))

    def get_all_indexes(self, ) -> list[int]:
        self.cursor.execute(f'SELECT {self.KEY_INDEX} FROM {self.NAME}')
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_sessions(self, ) -> list[Session]:
        self.cursor.execute(f'SELECT * FROM {self.NAME}')
        return [Session(index=int(row[0]), commands=eval(row[1])) for row in self.cursor.fetchall()]
