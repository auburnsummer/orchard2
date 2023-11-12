
from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator


class AddUserTable(Migrator):
    "Add user table"

    @property
    def migrate_from(self) -> str:
        return "origin"

    @property
    def migrate_to(self) -> str:
        return "aaaaa"

    def upgrade(self, conn: Connection):
        sql = """--sql
            CREATE TABLE "user"
            (
                "id" TEXT PRIMARY KEY NOT NULL,
                "name" TEXT NOT NULL,
                "cutoff" TEXT NOT NULL, -- datetime
                "avatar_url" TEXT, -- nullable
                CHECK( "id" LIKE 'u_%') -- ids for users begin with u_
            ) STRICT;
        """
        conn.execute(sql)
