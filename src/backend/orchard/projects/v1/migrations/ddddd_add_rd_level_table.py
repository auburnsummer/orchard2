
from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator
from orchard.libs.utils.relative_file import whereami

class AddRDLevelTable(Migrator):
    "Add rd level table"

    @property
    def migrate_from(self) -> str:
        return "ccccc"

    @property
    def migrate_to(self) -> str:
        return "ddddd"

    def upgrade(self, conn: Connection):
        with open(whereami() / "ddddd_add_rd_level_table.sql") as f:
            sql = f.read()
        conn.execute(sql)
