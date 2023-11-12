from unittest.mock import Mock
from apsw import Connection
from orchard.libs.melite.migrations.migrate import MELITE_TABLE, Migrator, create_melite_table, get_current_version, migrate
import pytest
import apsw

@pytest.fixture
def db():
    conn = apsw.Connection(":memory:")
    yield conn

@pytest.fixture
def db_with_existing_table(db):
    create_melite_table(db)
    db.execute(f"""
        UPDATE "{MELITE_TABLE}"
        SET "melite_version" = 'newversion'
        WHERE "id" = ?
    """, [0])
    yield db

@pytest.fixture
def mock_migrators():
    calls = []
    class StepOne(Migrator):
        @property
        def migrate_from(self) -> str:
            return "origin"

        @property
        def migrate_to(self) -> str:
            return "a"

        def upgrade(self, conn: Connection):
            calls.append("A")

    class StepTwo(Migrator):
        @property
        def migrate_from(self) -> str:
            return "a"

        @property
        def migrate_to(self) -> str:
            return "b"

        def upgrade(self, conn: Connection):
            calls.append("B")

    class StepThree(Migrator):
        @property
        def migrate_from(self) -> str:
            return "b"

        @property
        def migrate_to(self) -> str:
            return "c"

        def upgrade(self, conn: Connection):
            calls.append("C")

    # not in order on purpose.
    migrators = [StepThree(), StepOne(), StepTwo()]

    return migrators, calls

def test_get_current_version_returns_current_version_when_table_exists(db_with_existing_table):
    assert get_current_version(db_with_existing_table).melite_version == "newversion"

def test_get_current_version_returns_origin_when_table_does_not_exist(db):
    assert get_current_version(db).melite_version == "origin"

def test_migrate(db, mock_migrators):
    migrators, calls = mock_migrators
    migrate(db, None, migrators)

    v = get_current_version(db)
    assert v.melite_version == "c"
    # the migrations were called in the correct order.
    assert calls == ["A", "B", "C"]

def test_migrate_does_not_run_migrator_outside_of_requested_version(db, mock_migrators):
    migrators, calls = mock_migrators
    migrate(db, "b", migrators)
    v = get_current_version(db)
    assert v.melite_version == "b"
    # C not called.
    assert calls == ["A", "B"]


