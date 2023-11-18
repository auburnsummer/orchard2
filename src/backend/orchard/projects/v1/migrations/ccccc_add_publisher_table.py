
from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator


class AddPublisherTable(Migrator):
    "Add publisher table"

    @property
    def migrate_from(self) -> str:
        return "bbbbb"

    @property
    def migrate_to(self) -> str:
        return "ccccc"

    def upgrade(self, conn: Connection):
        sql = """--sql
            CREATE TABLE "publisher"
            (
                "id" TEXT PRIMARY KEY NOT NULL,
                "name" TEXT NOT NULL,
                "cutoff" TEXT NOT NULL, -- datetime
                CHECK( "id" LIKE 'p_%') -- ids for publishers begin with u_
            ) STRICT;
            --sql
            CREATE TABLE "discord_guild_publisher_credential"
            (
                "id" TEXT PRIMARY KEY NOT NULL,
                "publisher" TEXT NOT NULL REFERENCES "publisher" ("id")
            ) STRICT;
            --sql
            CREATE INDEX "discord_guild_publisher_credential_publisher_index" ON "discord_guild_publisher_credential" ("publisher")
        """
        conn.execute(sql)
