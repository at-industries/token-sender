from .tables.sessions import TableSessions
from .constants import FILENAME_DATABASE

import sqlite3 as sq


connection = sq.connect(FILENAME_DATABASE)
cursor = connection.cursor()

table_sessions = TableSessions(
    connection=connection,
    cursor=cursor,
)
