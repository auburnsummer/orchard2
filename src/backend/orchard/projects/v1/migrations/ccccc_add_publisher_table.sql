BEGIN TRANSACTION;

CREATE TABLE "publisher"
(
    "id" TEXT PRIMARY KEY NOT NULL,
    "name" TEXT NOT NULL,
    "cutoff" TEXT NOT NULL, -- datetime
    CHECK( "id" LIKE 'p_%') -- ids for publishers begin with u_
) STRICT;

CREATE TABLE "discord_guild_publisher_credential"
(
    "id" TEXT PRIMARY KEY NOT NULL,
    "publisher" TEXT NOT NULL REFERENCES "publisher" ("id")
) STRICT;

CREATE INDEX "discord_guild_publisher_credential_publisher_index" ON "discord_guild_publisher_credential" ("publisher");

COMMIT;