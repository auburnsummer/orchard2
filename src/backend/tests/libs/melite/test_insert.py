
from orchard.libs.melite.insert import insert
from orchard.libs.melite.select import Select
from tests.libs.melite.conftest import Bird, Song2, Tag, Watcher


def test_insert_basic_operation(db_with_one_table):
    to_insert = Bird(
        id="hhhhh",
        name="fairywren",
        height_cm=3,
        colour="blue"
    )
    insert(db_with_one_table, to_insert)

    # get it back.
    result = Select(db_with_one_table, Bird).by_id("hhhhh")
    assert result == to_insert

def test_insert_recurses_sub_structs_if_given(db_with_two_tables):
    to_insert = Watcher(
        id="66666",
        name="aoife",
        fav_bird=Bird(
            id="hhhhh",
            name="fairywren",
            height_cm=3,
            colour="blue"
        )
    )
    insert(db_with_two_tables, to_insert, True)
    result = Select(db_with_two_tables, Watcher).by_id("66666")
    assert result == to_insert

def test_insert_works_with_json_columns(db_with_table_with_array_column):
    song = Song2(
        id="mmmmm",
        name="mama",
        tags=[
            Tag(
                tag="my chemical romance",
                canonical=True
            ),
            Tag(
                tag="mcr",
                canonical=False
            )
        ]
    )
    insert(db_with_table_with_array_column, song)
    result = Select(db_with_table_with_array_column, Song2).by_id("mmmmm")
    assert result == song