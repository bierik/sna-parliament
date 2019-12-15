import contextlib
from contextlib import contextmanager
import sqlite3


@contextmanager
def connect():
    with contextlib.closing(sqlite3.connect('data.db')) as conn:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                yield (conn, cursor)


class Model:

    @classmethod
    def execute(cls, sql, obj=()):
        with connect() as (conn, cursor):
            cursor.execute(sql, obj)
            return cursor

    @classmethod
    def execute_many(cls, sql, objs=[]):
        with connect() as (conn, cursor):
            cursor.executemany(sql, objs)
            conn.commit()
            return cursor

    @classmethod
    def query(cls, sql, obj=()):
        with connect() as (conn, cursor):
            cursor.execute(sql, obj)
            return cursor.fetchall()

    @classmethod
    def global_id(cls, id):
        if type(id) is int:
            return id
        return id.split('-')[1]
