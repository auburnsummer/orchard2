BEGIN TRANSACTION;

CREATE TABLE "discord_credential"
(
    "id" TEXT PRIMARY KEY NOT NULL,
    "user" TEXT NOT NULL REFERENCES "user" ("id")
) STRICT;

CREATE INDEX "discord_credential_user_index" ON "discord_credential" ("user");

COMMIT;