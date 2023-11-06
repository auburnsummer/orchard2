from __future__ import annotations
from typing import Optional
from orchard.libs.melite.base import MeliteStruct

from orchard.libs.melite.factory import make_row_trace
import pytest


from apsw import Connection

@pytest.fixture
def db_with_one_table(db):
    q = """--sql
CREATE TABLE "bird" (
    "id" TEXT PRIMARY KEY NOT NULL,
    "name" TEXT NOT NULL,
    "height_cm" INT NOT NULL,
    "colour" TEXT NOT NULL
) STRICT;
    """
    db.execute(q)
    yield db

@pytest.fixture
def db_with_some_data(db_with_one_table):
    q = """--sql
INSERT INTO "bird"
VALUES 
    ('aaaaa', 'wren', 5, 'blue'),
    ('bbbbb', 'budgie', 6, 'green'),
    ('ccccc', 'miner', 11, 'black')
    """
    db_with_one_table.execute(q)
    yield db_with_one_table

class Bird(MeliteStruct):
    table_name = "bird"
    id: str
    name: str
    height_cm: int
    colour: str



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

@pytest.fixture
def db_with_two_tables(db_with_some_data):
    q = """--sql
CREATE TABLE "watcher" (
    "id" TEXT PRIMARY KEY NOT NULL,
    "name" TEXT NOT NULL,
    "fav_bird" TEXT,
    FOREIGN KEY("fav_bird") REFERENCES "bird"("id")
)
    """
    db_with_some_data.execute(q)
    yield db_with_some_data

class Watcher(MeliteStruct, kw_only=True):
    table_name = "watcher"
    id: str
    name: str
    fav_bird: Optional[Bird] = None

@pytest.fixture
def db_with_two_tables_and_data(db_with_two_tables):
    q = """--sql
INSERT INTO "watcher"
VALUES
    ('11111', 'mark', 'aaaaa'),
    ('22222', 'anna', 'ccccc'),
    ('33333', 'ines', 'aaaaa'),
    ('44444', 'birdhater3000', NULL)
    """
    db_with_two_tables.execute(q)
    yield db_with_two_tables

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

@pytest.fixture
def db_with_two_tables_not_null_fk(db_with_some_data):
    q = """--sql
CREATE TABLE "watcher" (
    "id" TEXT PRIMARY KEY NOT NULL,
    "name" TEXT NOT NULL,
    "fav_bird" TEXT NOT NULL,
    FOREIGN KEY("fav_bird") REFERENCES "bird"("id")
)
    """
    db_with_some_data.execute(q)
    yield db_with_some_data

@pytest.fixture
def db_with_two_tables_not_null_fk_and_data(db_with_two_tables_not_null_fk):
    q = """--sql
INSERT INTO "watcher"
VALUES
    ('11111', 'mark', 'aaaaa'),
    ('22222', 'anna', 'ccccc'),
    ('33333', 'ines', 'aaaaa')
    """
    db_with_two_tables_not_null_fk.execute(q)
    yield db_with_two_tables_not_null_fk

class Watcher2(MeliteStruct, kw_only=True):
    table_name = "watcher"
    id: str
    name: str
    fav_bird: Bird

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