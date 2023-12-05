CREATE TABLE "user"
(
    "id" TEXT PRIMARY KEY NOT NULL,
    "name" TEXT NOT NULL,
    "cutoff" TEXT NOT NULL, -- datetime
    "avatar_url" TEXT, -- nullable
    CHECK( "id" LIKE 'u_%') -- ids for users begin with u_
) STRICT;