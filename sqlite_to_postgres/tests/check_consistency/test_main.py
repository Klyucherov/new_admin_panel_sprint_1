import datetime
import os
import sqlite3
import sys

import psycopg2

filename = os.path.abspath(__file__)
currentdir = os.path.dirname(filename)
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

from connect_data import DSL
from db_class import SQLiteExtractor, PostgresSaver
from data_class import (
    Filmwork,
    Genre,
    Person,
    GenreFilmwork,
    PersonFilmwork,
)

from utils import ExtrFirstEls


def test_sql() -> None:
    dbpath = os.path.join(parentdir, "db.sqlite")

    with sqlite3.connect(dbpath) as sqlite_conn, psycopg2.connect(**DSL) as pg_conn:

        postgres_saver = PostgresSaver(pg_conn)
        sqlite_extractor = SQLiteExtractor(sqlite_conn)

        table_dataclass = [
            Filmwork,
            Genre,
            Person,
            GenreFilmwork,
            PersonFilmwork,
        ]

        for table in table_dataclass:
            g1 = sqlite_extractor.extract_yield(table)
            g2 = postgres_saver.extract_yield(table)

            while True:

                tbl1 = [it.to_tuple() for it in next(g1)]
                tbl2 = [table(*it).to_tuple() for it in next(g2)]

                if table.TableName() in ['genre_film_work', 'person_film_work']:
                    tbl2 = [table(*it).to_tuple() for it in tbl2]

                if len(tbl1) == 0 or len(tbl2) == 0:
                    break

                assert len(tbl1) == len(tbl2)

                for it in tbl1:
                    index = ExtrFirstEls([i for i, e in enumerate(tbl2) if e[0] == it[0]])
                    assert not index is None

                    itt = tbl2[index]

                    a = [el.replace(tzinfo=None) if isinstance(el, datetime.datetime) else el for el in it]
                    b = [el.replace(tzinfo=None) if isinstance(el, datetime.datetime) else el for el in itt]

                    assert a == b


if __name__ == '__main__':
    test_sql()
