from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator
from orchard.libs.utils.relative_file import whereami

class AddDiscordCredentialsTable(Migrator):
    "Add discord credentials table"

    @property
    def migrate_from(self) -> str:
        return "aaaaa"

    @property
    def migrate_to(self) -> str:
        return "bbbbb"

    def upgrade(self, conn: Connection):
        with open(whereami() / "bbbbb_add_discord_credentials_table.sql") as f:
            sql = f.read()
        conn.execute(sql)
