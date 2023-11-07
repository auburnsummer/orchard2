from typing import Optional
from orchard.libs.melite.base import MeliteStruct
import pytest
import apsw

import apsw.bestpractice


@pytest.fixture
def db():
    "initial db"
    apsw.bestpractice.apply(apsw.bestpractice.recommended)
    conn = apsw.Connection(":memory:")
    yield conn


@pytest.fixture
def db_with_one_table(db: apsw.Connection):
    "make bird table"
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
def db_with_some_data(db_with_one_table: apsw.Connection):
    "insert into bird table"
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
    "corresponds to bird table"
    table_name = "bird"
    id: str
    name: str
    height_cm: int
    colour: str


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