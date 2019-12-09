import contextlib
import sqlite3


class Model:
    @classmethod
    def query(cls, sql, obj=()):
        with contextlib.closing(sqlite3.connect('data.db')) as conn:
            with conn:
                with contextlib.closing(conn.cursor()) as cursor:
                    cursor.execute(sql, obj)
                    return cursor
