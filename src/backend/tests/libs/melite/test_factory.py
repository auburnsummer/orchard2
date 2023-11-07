from __future__ import annotations

from orchard.libs.melite.factory import make_row_trace

from apsw import Connection
from tests.libs.melite.conftest import Bird, Song, Watcher, Watcher2


def test_factory_basic_operation(db_with_some_data: Connection):
    cursor = db_with_some_data.cursor()
    cursor.set_row_trace(make_row_trace(Bird, db_with_some_data))
    q = """--sql
    SELECT * FROM bird
    """
    cursor.execute(q)
    results = list(cursor)
    assert results == [
        Bird(
            id="aaaaa",
            name="wren",
            height_cm=5,
            colour="blue"
        ),
        Bird(
            id="bbbbb",
            name="budgie",
            height_cm=6,
            colour="green"
        ),
        Bird(
            id="ccccc",
            name="miner",
            height_cm=11,
            colour="black"
        )
    ]


def test_factory_fk(db_with_two_tables_and_data):
    cursor = db_with_two_tables_and_data.cursor()
    cursor.set_row_trace(make_row_trace(Watcher, db_with_two_tables_and_data))
    q = """--sql
    SELECT * FROM watcher
    """
    cursor.execute(q)
    results = list(cursor)
    assert results == [
        Watcher(
            id="11111",
            name="mark",
            fav_bird=Bird(
                id="aaaaa",
                name="wren",
                height_cm=5,
                colour="blue"
            ),
        ),
        Watcher(
            id="22222",
            fav_bird=Bird(
                id="ccccc",
                name="miner",
                height_cm=11,
                colour="black"
            ),
            name="anna"
        ),
        Watcher(id='33333', name='ines', fav_bird=Bird(id='aaaaa', name='wren', height_cm=5, colour='blue')),
        Watcher(id='44444', name='birdhater3000', fav_bird=None)
    ]


def test_factory_fk_not_null(db_with_two_tables_not_null_fk_and_data):
    cursor = db_with_two_tables_not_null_fk_and_data.cursor()
    cursor.set_row_trace(make_row_trace(Watcher2, db_with_two_tables_not_null_fk_and_data))
    q = """--sql
    SELECT * FROM watcher
    """
    cursor.execute(q)
    results = list(cursor)
    assert results == [
        Watcher2(
            id="11111",
            name="mark",
            fav_bird=Bird(
                id="aaaaa",
                name="wren",
                height_cm=5,
                colour="blue"
            ),
        ),
        Watcher2(
            id="22222",
            fav_bird=Bird(
                id="ccccc",
                name="miner",
                height_cm=11,
                colour="black"
            ),
            name="anna"
        ),
        Watcher2(id='33333', name='ines', fav_bird=Bird(id='aaaaa', name='wren', height_cm=5, colour='blue')),
    ]


def test_factory_array_column(db_with_array_col_table_data: Connection):
    cursor = db_with_array_col_table_data.cursor()
    cursor.set_row_trace(make_row_trace(Song, db_with_array_col_table_data))
    q = """--sql
    SELECT * FROM song
    """
    cursor.execute(q)
    results = list(cursor)
    assert results == [
        Song(id='fffff', name='tell me how', tags=['slow', '1p']),
        Song(id='ggggg', name='evan finds the third room', tags=['fast', 'gimmick'])
    ]