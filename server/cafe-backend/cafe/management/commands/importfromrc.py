from tempfile import NamedTemporaryFile

import django
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from cafe.models import Club, User, RDLevel
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.models.rdlevels.tempuser import get_or_create_discord_user
from cafe.tasks.run_prefill import run_prefill
from vitals import vitals

from loguru import logger

from orchard.settings import DISCORD_BOT_TOKEN
from functools import cache

from multiprocessing import Pool

import json

DB_URL = "https://api2.rhythm.cafe/datasette/combined.db"

DISCORD_GET_USER_API = "https://discord.com/api/v10/users"

import sqlite3

import httpx

import tenacity


@cache
@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def get_discord_user_from_id(discord_user_id: str) -> User:
    # e.g. https://discord.com/api/v10/users/832410474955014144
    url = f"{DISCORD_GET_USER_API}/{discord_user_id}"
    response = httpx.get(url, headers={"Authorization": f"Bot {DISCORD_BOT_TOKEN}"})
    response.raise_for_status()
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
    if not prefill.ready:
        logger.warning(f"Prefill failed for level {prefill.id} ")
        logger.warning(prefill.errors)
        return
    level_data = {
        **prefill.data,
        "approval": existing_approval,
        "submitter": prefill.user,
        "club": prefill.club
    }
    if level_data['icon_url'] is None:
        level_data['icon_url'] = ''
    try:
        RDLevel.objects.create(**level_data)
    except IntegrityError:
        # dunno why but this only appears if we use print() and not logger.info
        print(f"Level already exists")
    finally:
        prefill.delete()


class Command(BaseCommand):
    """
    Import legacy levels from rhythm cafe
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--club-id',
            type=str,
            required=True,
            help='ID for the club which will hold rc1 levels'
        )
        parser.add_argument(
            '--user-id',
            type=str,
            required=True,
            help='ID for the user which will hold spreadsheet levels'
        )

    def handle(self, *args, **options):
        logger.info("this needs to talk to typesense!")
        logger.info("so if you're running this locally, make sure to have the stack running first")
        club_id = options['club_id']
        club = Club.objects.get(id=club_id)
        user_id = options['user_id']
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
            with Pool(6, initializer=django.setup) as pool:
                for row in res:
                    discord_user = None
                    sha1 = row['sha1']
                    try:
                        existing_level = RDLevel.objects.get(sha1=sha1)
                        if existing_level.approval == 0 and row['approval'] != 0:
                            existing_level.approval = row['approval']
                            existing_level.save()
                        continue
                    except RDLevel.DoesNotExist:
                        pass
                    logger.info(f"Processing level {row['song']} ({row['id']})")
                    if row['source'] == 'rdl':
                        rdl_data = json.loads(row['source_metadata'])
                        discord_user_id = rdl_data['user_id']
                        discord_user = get_discord_user_from_id(discord_user_id)

                    pool.apply_async(
                        process_legacy_level,
                        args=(row['url2'], discord_user or user, club, row['approval'])
                    )

                pool.close()
                pool.join()
            conn.close()