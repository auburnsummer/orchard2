from apsw import Connection
from orchard.libs.melite.select import Select
from tests.libs.melite.conftest import Bird

def test_select_by_id_returns_a_struct(db_with_some_data: Connection):
    result = Select(db_with_some_data, Bird).by_id("aaaaa")
    assert result is not None
    assert result == Bird(
        id="aaaaa",
        name="wren",
        height_cm=5,
        colour="blue"
    )

def test_select_by_id_returns_none_when_does_not_exist(db_with_some_data: Connection):
    result = Select(db_with_some_data, Bird).by_id("nope")
    assert result is None