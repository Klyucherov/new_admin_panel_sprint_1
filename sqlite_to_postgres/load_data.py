import os
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection

from connect_data import DSL
from data_class import (
    Filmwork,
    Genre,
    Person,
    GenreFilmwork,
    PersonFilmwork,
)
from db_class import PostgresSaver, SQLiteExtractor


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    table_dataclass = [
        Filmwork,
        Genre,
        Person,
        GenreFilmwork,
        PersonFilmwork,
    ]

    for table in table_dataclass:

        for data in sqlite_extractor.extract_yield(table):
            postgres_saver.save_all_data(table, data)


if __name__ == '__main__':
    filename = os.path.abspath(__file__)
    dbdir = os.path.dirname(filename)
    dbpath = os.path.join(dbdir, "db.sqlite")

    with sqlite3.connect(dbpath) as sqlite_conn, psycopg2.connect(**DSL) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
