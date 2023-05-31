import dataclasses
import sqlite3
from typing import Generator

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from psycopg2.extras import execute_batch

from const import PAGE_SIZE


class SQLiteExtractor(object):

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.con = connection.cursor()
        self.cur = self.con

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback) -> None:
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()

    def extract(self, sql: str) -> list:
        try:
            self.cur.execute(sql)
            record = self.cur.fetchall()
            return record
        except:
            return []

    def extract_yield(self, table: dataclasses.dataclass) -> Generator:

        self.cur.row_factory = lambda c, r: table(*r)
        sql = f'select * from {table.TableName()};'

        self.cur.execute(sql)

        while results := self.cur.fetchmany(100):
            yield results

        yield []


class PostgresSaver(object):

    def __init__(self, pg_conn: _connection) -> None:
        self.con = pg_conn
        self.cur = self.con.cursor(cursor_factory=DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback) -> None:
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()

    def save_all_data(self, table: dataclasses.dataclass, data: list) -> None:

        c = len(list(table.__dict__['__dataclass_fields__']))
        count_s = ','.join(['%s'] * c)

        query = f""
        query += f" insert into {table.TableName()}"
        query += f" VALUES ({count_s})"
        query += f" ON CONFLICT (id) DO NOTHING; "

        data = [it.to_tuple() for it in data]

        try:
            execute_batch(self.cur, query, data, page_size=PAGE_SIZE)
            self.con.commit()
            return True
        except Exception as e:
            self.con.commit()
            return False

    def save_one(self, query, elem) -> None:
        try:
            self.cur.execute(query, elem)
            self.con.commit()
            return True
        except Exception as e:
            self.con.commit()
            return False

    def extract(self, sql: str) -> list:
        try:
            self.cur.execute(sql)
            record = self.cur.fetchall()
            return record
        except:
            return []

    def extract_yield(self, table: dataclasses.dataclass) -> Generator:

        sql = f'select * from {table.TableName()};'

        self.cur.execute(sql)

        while results := self.cur.fetchmany(100):
            yield results

        yield []
