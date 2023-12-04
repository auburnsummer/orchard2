"""
Test data generator.
This uses test_data.json which is a dump of the first 1000 rows from rhythm cafe v1.

To make the test data, we mix them around in a demented ad libs.

to use this: python -m orchard.projects.v1.tools.generate_test_data
"""

from datetime import datetime, timezone
import msgspec
from pathlib import Path
import random
import json

from orchard.projects.v1.models.engine import insert, setup_db
from orchard.projects.v1.models.users import User
from orchard.projects.v1.models.publishers import Publisher
from orchard.projects.v1.models.rd_levels import RDLevel
from orchard.libs.utils.gen_id import IDType, gen_id

from loguru import logger

NUMBER_OF_USERS = 200
NUMBER_OF_LEVELS = 1000

def gen_user_name():
    return "TESTUSER " + "".join(random.choice("abcdefghijklmnopqratuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10))

def gen_sha1():
    return "".join(random.choice("0123456789abcdef") for _ in range(40))

def gen_alt_song():
    return "ALTTITLE " + "".join(random.choice("abcdefghijklmnopqratuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10))


def main_test_data_gen(data):
    users = [User.create(gen_user_name()) for _ in range(NUMBER_OF_USERS)]

    pub1 = Publisher.create("New York State Library")
    pub2 = Publisher.create("Australian Music Examinations Board")

    artist_pool = [
        {
            "artist": row["artist"],
            "artist_tokens": json.loads(row["artist_tokens"]),
        } for row in data
    ]

    song_pool = [row["song"] for row in data]
    description_pool = [row["description"] for row in data]

    authors_pool = [
        {
            "authors": json.loads(row["authors"]),
            "authors_raw": row["authors"]
        } for row in data
    ]

    tag_pool = [row["tags"] for row in data]


    for i in range(NUMBER_OF_LEVELS):
        logger.info(f"Making level {i}")
        artist_pick = random.choice(artist_pool)
        authors_pick = random.choice(authors_pool)
        if random.random() > 0.9:
            min_bpm = random.uniform(60.0, 300.0)
            max_bpm = min_bpm
        else:
            min_bpm = random.uniform(60.0, 90.0)
            max_bpm = random.uniform(min_bpm, 300.0)

        if random.random() > 0.1:
            song_alt = ""
        else:
            song_alt = gen_alt_song()

        single_player = random.choice([True, False])
        if single_player is False:
            two_player = True
        else:
            two_player = random.choice([True, False])
        level = RDLevel(
            id=gen_id(id_type=IDType.RD_LEVEL),
            artist=artist_pick["artist"],
            artist_tokens=artist_pick["artist_tokens"],
            song=random.choice(song_pool),
            seizure_warning=random.choice([True, False]),
            description=random.choice(description_pool),
            hue=random.random(),
            authors=authors_pick["authors"],
            authors_raw=authors_pick["authors_raw"],
            max_bpm=max_bpm,
            min_bpm=min_bpm,
            difficulty=random.choice([0, 1, 2, 3]),
            single_player=single_player,
            two_player=two_player,
            last_updated=datetime.now(tz=timezone.utc),
            tags=random.choice(tag_pool),
            has_classics=random.choice([True, False]),
            has_oneshots=random.choice([True, False]),
            has_squareshots=random.choice([True, False]),
            has_freezeshots=random.choice([True, False]),
            has_freetimes=random.choice([True, False]),
            has_holds=random.choice([True, False]),
            has_skipshots=random.choice([True, False]),
            has_window_dance=random.choice([True, False]),
            sha1=gen_sha1(),
            rdlevel_sha1=gen_sha1(),
            is_animated=random.choice([True, False]),

            image="https://placehold.co/1377x768/png?text=Placeholder+Thumbnail",
            thumb="https://placehold.co/640x480/webp?text=Placeholder+Thumbnail",
            icon="https://placehold.co/48x48/png?text=Icon",

            url="http://rhythmdr.com/example.rdzip",

            song_alt=song_alt,

            uploader=random.choice(users),
            publisher=random.choice([pub1, pub2]),

            uploaded=datetime.now(tz=timezone.utc),

            approval=random.choice([0, 10]),
        )

        insert(level, False)

if __name__ == "__main__":
    path = Path(__file__).resolve().parent
    test_data_json_path = path / "test_data.json"
    with open(test_data_json_path) as f:
        data = msgspec.json.decode(f.read())

    setup_db()

    main_test_data_gen(data)