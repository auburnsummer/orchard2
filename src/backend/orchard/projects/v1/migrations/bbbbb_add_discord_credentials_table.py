from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator

class AddDiscordCredentialsTable(Migrator):
    "Add discord credentials table"

    @property
    def migrate_from(self) -> str:
        return "aaaaa"

    @property
    def migrate_to(self) -> str:
        return "bbbbb"

    def upgrade(self, conn: Connection):
        sql = """--sql
            CREATE TABLE "discord_credential"
            (
                "id" TEXT PRIMARY KEY NOT NULL,
                "user" TEXT NOT NULL REFERENCES "user" ("id")
            ) STRICT;
        """
        conn.execute(sql)
