from orchard.libs.melite.insert import insert
from orchard.libs.melite.select import Select
from orchard.libs.melite.update import update
from tests.libs.melite.conftest import Bird, Song2, Tag, Watcher


def test_update_basic_operation(db_with_one_table):
    # from test_insert.py
    to_insert = Bird(
        id="hhhhh",
        name="fairywren",
        height_cm=3,
        colour="blue"
    )
    insert(db_with_one_table, to_insert)

    to_insert2 = Bird(
        id="ggggg",
        name="fairywrena",
        height_cm=4,
        colour="blue"
    )
    insert(db_with_one_table, to_insert2)


    # now let's edit it
    to_insert.name = "fairy wren"
    update(db_with_one_table, to_insert)

    value = Select(db_with_one_table, Bird).by_id("hhhhh")
    assert value is not None
    assert value.name == "fairy wren"

    # check the other one was not affected by the insert
    value2 = Select(db_with_one_table, Bird).by_id("ggggg")
    assert value2 == to_insert2

def test_update_recursive(db_with_two_tables):
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

    # now edit both!
    to_insert.fav_bird.colour = "yellow"
    to_insert.name = "aisling"
    update(db_with_two_tables, to_insert, True)

    result = Select(db_with_two_tables, Watcher).by_id("66666")
    assert result == to_insert

def test_update_json_column(db_with_table_with_array_column):
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
    
    song.tags[1].tag = "paramore"
    update(db_with_table_with_array_column, song)
    
    result = Select(db_with_table_with_array_column, Song2).by_id("mmmmm")
    assert result == song