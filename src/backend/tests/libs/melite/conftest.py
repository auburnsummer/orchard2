from typing import Annotated, List, Optional
import msgspec
from orchard.libs.melite.base import JSON, MeliteStruct
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


@pytest.fixture
def db_with_table_with_array_column(db):
    q = """--sql
CREATE TABLE "song" (
    "id" TEXT PRIMARY KEY NOT NULL,
    "name" TEXT NOT NULL,
    "tags" TEXT NOT NULL -- this is a json encoded column, but sqlite doesn't know that!
) STRICT
    """
    db.execute(q)
    yield db

@pytest.fixture
def db_with_array_col_table_data(db_with_table_with_array_column):
    q = """--sql
    INSERT INTO "song"
    VALUES
        ('fffff', 'tell me how', '["slow","1p"]'),
        ('ggggg', 'evan finds the third room', '["fast","gimmick"]')
    """
    db_with_table_with_array_column.execute(q)
    yield db_with_table_with_array_column

class Song(MeliteStruct, kw_only=True):
    table_name = "song"
    id: str
    name: str
    tags: Annotated[List[str], JSON]

class Tag(msgspec.Struct, kw_only=True):
    tag: str
    canonical: bool

class Song2(MeliteStruct, kw_only=True):
    table_name = "song"
    id: str
    name: str
    tags: Annotated[List[Tag], JSON]

@pytest.fixture
def db_with_array_struct_col_table_data(db_with_table_with_array_column):
    q = """--sql
    INSERT INTO "song"
    VALUES
        ('fffff', 'tell me how', '[{"tag":"slow","canonical":true},{"tag": "1p","canonical":true}]'),
        ('ggggg', 'evan finds the third room', '[{"tag":"fast","canonical":true},{"tag":"the third room is ao3","canonical":false}]')
    """
    db_with_table_with_array_column.execute(q)
    yield db_with_table_with_array_column
