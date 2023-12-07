BEGIN TRANSACTION;
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
    "sha1"              TEXT        NOT NULL UNIQUE, -- hex string
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
    CHECK( "id" LIKE 'rd_%'), -- ids for rdlevels begin with rd_
    CHECK( "max_bpm" >= "min_bpm" ) 
) STRICT;

CREATE INDEX "rdlevel_idx_last_updated" ON "rdlevel" ("last_updated");
CREATE INDEX "rdlevel_idx_uploader" ON "rdlevel" ("uploader");
CREATE INDEX "rdlevel_idx_publisher" ON "rdlevel" ("publisher");
CREATE INDEX "rdlevel_idx_sha1" ON "rdlevel" ("sha1");
CREATE INDEX "rdlevel_idx_max_bpm" ON "rdlevel" ("max_bpm");
CREATE INDEX "rdlevel_idx_superindex" ON "rdlevel" ("approval","difficulty", "single_player", "two_player", "has_classics", "has_oneshots", 
"has_squareshots", "has_freezeshots", "has_freetimes", "has_holds", "has_skipshots", "has_window_dance", "seizure_warning");

-- fts
CREATE VIRTUAL TABLE rdlevel_search USING fts5(
    "id" UNINDEXED,
    "song",
    "song_alt",
    "artist_tokens",
    "authors",
    "description",
    "tags",
    prefix='2 3',
    tokenize='porter signal_tokenizer'
);
-- configure the rank: https://www.sqlite.org/fts5.html#the_rank_configuration_option
INSERT INTO rdlevel_search(rdlevel_search, rank) VALUES('rank', 'bm25(0.0, 6.0, 6.0, 2.0, 2.0, 1.0, 3.0)');

CREATE TRIGGER rdlevel_ai AFTER INSERT ON rdlevel BEGIN
    INSERT INTO rdlevel_search ("id", "song", "song_alt", "artist_tokens", "authors", "description", "tags")
        VALUES (new.id, new.song, new.song_alt, new.artist_tokens, new.authors, new.description, new.tags);
END;

CREATE TRIGGER rdlevel_ad AFTER DELETE on rdlevel BEGIN
    DELETE FROM rdlevel_search WHERE rdlevel_search.id = old.id;
END;

CREATE TRIGGER rdlevel_au AFTER UPDATE on rdlevel BEGIN
    DELETE FROM rdlevel_search WHERE rdlevel_search.id = old.id;
    INSERT INTO rdlevel_search ("id", "song", "song_alt", "artist_tokens", "authors", "description", "tags")
        VALUES (new.id, new.song, new.song_alt, new.artist_tokens, new.authors, new.description, new.tags);
END;


-- tags
CREATE TABLE "rdlevel_tag"
(
    "rdlevel"   TEXT    NOT NULL REFERENCES "rdlevel" ("id"),
    "tag"       TEXT    NOT NULL,
    PRIMARY KEY ("rdlevel", "tag")
);

CREATE INDEX "rdlevel_tag_idx_tag" ON "rdlevel_tag" ("tag");

CREATE TRIGGER rdlevel_ai2 AFTER INSERT ON rdlevel BEGIN
  INSERT OR IGNORE INTO rdlevel_tag(rdlevel, tag) select new.id, j.value from json_each(new.tags) as j;
END;

CREATE TRIGGER rdlevel_ad2 AFTER DELETE ON rdlevel BEGIN
  DELETE FROM rdlevel_tag where rdlevel = old.id;
END;

CREATE TRIGGER rdlevel_au2 AFTER UPDATE ON rdlevel BEGIN
  DELETE FROM rdlevel_tag where rdlevel = old.id;
  INSERT OR IGNORE INTO rdlevel_tag(rdlevel, tag) select new.id, j.value from json_each(new.tags) as j;
END;

--artists
CREATE TABLE "rdlevel_artist"
(
    "rdlevel"       TEXT    NOT NULL REFERENCES "rdlevel" ("id"),
    "artist"        TEXT    NOT NULL,
    PRIMARY KEY ("rdlevel", "artist")
);

CREATE INDEX "rdlevel_artist_idx_artist" ON "rdlevel_artist" ("artist");

CREATE TRIGGER rdlevel_ai3 AFTER INSERT ON rdlevel BEGIN
  INSERT OR IGNORE INTO rdlevel_artist(rdlevel, artist) select new.id, j.value from json_each(new.artist_tokens) as j;
END;

CREATE TRIGGER rdlevel_ad3 AFTER DELETE ON rdlevel BEGIN
  DELETE FROM rdlevel_artist where rdlevel = old.id;
END;

CREATE TRIGGER rdlevel_au3 AFTER UPDATE ON rdlevel BEGIN
  DELETE FROM rdlevel_artist where rdlevel = old.id;
  INSERT OR IGNORE INTO rdlevel_artist(rdlevel, artist) select new.id, j.value from json_each(new.artist_tokens) as j;
END;

--authors
CREATE TABLE "rdlevel_author"
(
    "rdlevel"       TEXT    NOT NULL REFERENCES "rdlevel" ("id"),
    "author"        TEXT    NOT NULL,
    PRIMARY KEY ("rdlevel", "author")
);

CREATE INDEX "rdlevel_author_idx_author" ON "rdlevel_author" ("author");

CREATE TRIGGER rdlevel_ai4 AFTER INSERT ON rdlevel BEGIN
  INSERT OR IGNORE INTO rdlevel_author(rdlevel, author) select new.id, j.value from json_each(new.authors) as j;
END;

CREATE TRIGGER rdlevel_ad4 AFTER DELETE ON rdlevel BEGIN
  DELETE FROM rdlevel_author where rdlevel = old.id;
END;

CREATE TRIGGER rdlevel_au4 AFTER UPDATE ON rdlevel BEGIN
  DELETE FROM rdlevel_author where rdlevel = old.id;
  INSERT OR IGNORE INTO rdlevel_author(rdlevel, author) select new.id, j.value from json_each(new.authors) as j;
END;


COMMIT;