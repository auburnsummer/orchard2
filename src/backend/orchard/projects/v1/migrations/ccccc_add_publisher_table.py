
from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator
from orchard.libs.utils.relative_file import whereami


class AddPublisherTable(Migrator):
    "Add publisher table"

    @property
    def migrate_from(self) -> str:
        return "bbbbb"

    @property
    def migrate_to(self) -> str:
        return "ccccc"

    def upgrade(self, conn: Connection):
        with open(whereami() / "ccccc_add_publisher_table.sql") as f:
            sql = f.read()

        conn.execute(sql)
