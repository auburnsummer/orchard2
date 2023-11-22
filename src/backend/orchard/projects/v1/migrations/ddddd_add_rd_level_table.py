
from apsw import Connection
from orchard.libs.melite.migrations.migrate import Migrator


class AddRDLevelTable(Migrator):
    "Add rd level table"

    @property
    def migrate_from(self) -> str:
        return "ccccc"

    @property
    def migrate_to(self) -> str:
        return "ddddd"

    def upgrade(self, conn: Connection):
        sql = """--sql
            CREATE TABLE "rdlevel"
            (
                "id"                TEXT        PRIMARY KEY NOT NULL,
                "artist"            TEXT        NOT NULL,
                "artist_tokens"     TEXT        NOT NULL, -- json
                "song"              TEXT        NOT NULL,
                "seizure_warning"   INTEGER     NOT NULL, -- boolean
                "description"       TEXT        NOT NULL,
                "hue"               REAL        NOT NULL,
                "authors"           TEXT        NOT NULL, -- json
                "authors_raw"       TEXT        NOT NULL,
                "max_bpm"           REAL        NOT NULL,
                "min_bpm"           REAL        NOT NULL,
                "difficulty"        INTEGER     NOT NULL,
                "single_player"     INTEGER     NOT NULL, -- boolean
                "two_player"        INTEGER     NOT NULL, -- boolean
                "last_updated"      TEXT        NOT NULL, -- datetime
                "tags"              TEXT        NOT NULL, -- json
                "has_classics"      INTEGER     NOT NULL, -- boolean
                "has_oneshots"      INTEGER     NOT NULL, -- boolean
                "has_squareshots"   INTEGER     NOT NULL, -- boolean
                "has_freezeshots"   INTEGER     NOT NULL, -- boolean
                "has_freetimes"     INTEGER     NOT NULL, -- boolean
                "has_holds"         INTEGER     NOT NULL, -- boolean
                "has_skipshots"     INTEGER     NOT NULL, -- boolean
                "has_window_dance"  INTEGER     NOT NULL, -- boolean
                "sha1"              TEXT        NOT NULL, -- hex string
                "rdlevel_sha1"      TEXT        NOT NULL, -- hex string
                "is_animated"       INTEGER     NOT NULL, -- boolean
                "image"             TEXT        NOT NULL, -- url
                "thumb"             TEXT        NOT NULL, -- url
                "icon"              TEXT        , -- nullable
                "url"               TEXT        NOT NULL, -- to the .rdzip

                "song_alt"          TEXT        NOT NULL,
                "uploader"          TEXT        NOT NULL REFERENCES "user" ("id"),
                "publisher"         TEXT        NOT NULL REFERENCES "publisher" ("id"),
                "uploaded"          TEXT        NOT NULL, -- datetime
                "approval"          INTEGER     NOT NULL,
                CHECK( "id" LIKE 'rd_%') -- ids for rdlevels begin with rd_
            ) STRICT;
            --sql
            CREATE INDEX "rdlevel_uploader_idx" ON "rdlevel" ("uploader");
            --sql
            CREATE INDEX "rdlevel_publisher_idx" ON "rdlevel" ("publisher");
        """
        conn.execute(sql)
