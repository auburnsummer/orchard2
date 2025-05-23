from tempfile import NamedTemporaryFile

from django.core.management.base import BaseCommand

from cafe.models import Club, User
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.tasks.run_prefill import run_prefill
from vitals import vitals

DB_URL = "https://api.rhythm.cafe/datasette/combined.db"

import sqlite3

import httpx

def process_legacy_level(level_url: str, user: User, club: Club) -> None:
    prefill = RDLevelPrefillResult.objects.create(
        url=level_url,
        version=1,
        user=user,
        prefill_type='new',
        club=club
    )
    run_prefill.call_local(prefill.id)
    prefill.refresh_from_db()
    print(prefill.data)


class Command(BaseCommand):
    """
    Import legacy levels from rhythm cafe
    """

    def handle(self, *args, **options):
        print("this needs to talk to meilisearch!")
        print("so if you're running this locally, make sure to have the stack running first")
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
            row = res.fetchone()
            print(row)
            process_legacy_level(row['url2'], user, club)