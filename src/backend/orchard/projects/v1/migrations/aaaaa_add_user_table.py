
from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator
from orchard.libs.utils.relative_file import whereami


class AddUserTable(Migrator):
    "Add user table"

    @property
    def migrate_from(self) -> str:
        return "origin"

    @property
    def migrate_to(self) -> str:
        return "aaaaa"

    def upgrade(self, conn: Connection):
        with open(whereami() / "aaaaa_add_user_table.sql") as f:
            sql = f.read()
        conn.execute(sql)
