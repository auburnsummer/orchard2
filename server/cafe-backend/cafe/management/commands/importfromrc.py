from tempfile import NamedTemporaryFile

from django.core.management.base import BaseCommand

from cafe.models import Club, User, RDLevel
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.models.rdlevels.tempuser import get_or_create_discord_user
from cafe.tasks.run_prefill import run_prefill
from vitals import vitals

from loguru import logger

from orchard.settings import DISCORD_BOT_TOKEN
from functools import cache

import json

DB_URL = "https://api2.rhythm.cafe/datasette/combined.db"

DISCORD_GET_USER_API = "https://discord.com/api/v10/users"

import sqlite3

import httpx


@cache
def get_discord_user_from_id(discord_user_id: str) -> User:
    # e.g. https://discord.com/api/v10/users/832410474955014144
    url = f"{DISCORD_GET_USER_API}/{discord_user_id}"
    response = httpx.get(url, headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"})
    body = response.json()
    global_name = body.get('global_name') or body.get('username')
    return get_or_create_discord_user(discord_user_id, global_name)


def process_legacy_level(level_url: str, user: User, club: Club, existing_approval: int) -> None:
    prefill = RDLevelPrefillResult.objects.create(
        url=level_url,
        version=1,
        user=user,
        prefill_type='new',
        club=club
    )
    run_prefill.call_local(prefill.id)
    prefill.refresh_from_db()
    level_data = {
        **prefill.data,
        "approval": existing_approval,
        "submitter": prefill.user,
        "club": prefill.club
    }
    if level_data['icon_url'] is None:
        level_data['icon_url'] = ''
    RDLevel.objects.create(**level_data)


class Command(BaseCommand):
    """
    Import legacy levels from rhythm cafe
    """

    def handle(self, *args, **options):
        logger.info("this needs to talk to meilisearch!")
        logger.info("so if you're running this locally, make sure to have the stack running first")
        club_id = input("enter the id for the club which will hold rc1 levels: ")
        club = Club.objects.get(id=club_id)
        user_id = input("enter the id for the user which will hold spreadsheet levels: ")
        user = User.objects.get(id=user_id)
        with NamedTemporaryFile(mode="w+b") as f:
            contents = httpx.get(DB_URL).content
            f.write(contents)
            f.flush()
            f.seek(0)
            conn = sqlite3.connect(f.name)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            res = cur.execute("SELECT * FROM combined")
            for row in res:
                logger.info(f"Processing level {row['song']} ({row['id']})")

                discord_user = None
                sha1 = row['sha1']
                try:
                    existing_level = RDLevel.objects.get(sha1=sha1)
                    logger.info(f"found existing level {existing_level}, therefore skipping")
                    continue
                except RDLevel.DoesNotExist:
                    pass
                if row['source'] == 'rdl':
                    rdl_data = json.loads(row['source_metadata'])
                    discord_user_id = rdl_data['user_id']
                    discord_user = get_discord_user_from_id(discord_user_id)
                process_legacy_level(row['url2'], discord_user or user, club, row['approval'])