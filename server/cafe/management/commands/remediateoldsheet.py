# a one time task I hope
import json
import re
import sqlite3
from tempfile import NamedTemporaryFile

import httpx
from django.core.management.base import BaseCommand
from loguru import logger

from cafe.models import RDLevel
from cafe.models.rdlevels.tempuser import get_or_create_discord_user
from cafe.models.user import User

DB_URL = "https://api2.rhythm.cafe/datasette/combined.db"

ATTACHMENT_URL_RE = re.compile(
    r'https://cdn\.discordapp\.com/attachments/\d+/(\d+)/'
)


def extract_attachment_id(url: str) -> str | None:
    m = ATTACHMENT_URL_RE.search(url)
    return m.group(1) if m else None


def build_attachment_mapping_from_data(data: dict) -> dict[str, tuple[str, str]]:
    """
    Parse a Discord channel export dict and return a mapping of
    attachment_id -> (discord_user_id, display_name).
    """
    mapping: dict[str, tuple[str, str]] = {}
    for msg in data['messages']:
        author_id = msg['author']['id']
        display_name = msg['author'].get('name')
        for att in msg.get('attachments', []):
            mapping[att['id']] = (author_id, display_name)
    return mapping


def build_attachment_mapping(json_path: str) -> dict[str, tuple[str, str]]:
    with open(json_path) as f:
        return build_attachment_mapping_from_data(json.load(f))


class Command(BaseCommand):
    """
    Assign sheet levels (yeoldesheet) to the Discord submitters
    using a Discord channel export

    The discord channel export uses https://github.com/tyrrrz/discordchatexporter format
    (which doesn't have global_name for some reason? so we use the name)
    """

    def add_arguments(self, parser):
        json_source = parser.add_mutually_exclusive_group(required=True)
        json_source.add_argument(
            '--json-file',
            type=str,
            help='Path to a local Discord channel export JSON (DiscordChatExporter format)',
        )
        json_source.add_argument(
            '--json-url',
            type=str,
            help='URL to fetch the Discord channel export JSON from',
        )
        parser.add_argument(
            '--db-path',
            type=str,
            default=None,
            help='Path to the local combined.db. If omitted, downloads from the live API.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Print what would be changed without writing to the database.',
        )

    def handle(self, *args, **options):
        db_path = options['db_path']
        dry_run = options['dry_run']

        if dry_run:
            logger.info("DRY RUN! no changes will be written")

        if options['json_file']:
            logger.info(f"Building attachment -> user mapping from {options['json_file']}")
            attachment_map = build_attachment_mapping(options['json_file'])
        else:
            logger.info(f"Building attachment -> user mapping from {options['json_url']}")
            response = httpx.get(options['json_url'])
            response.raise_for_status()
            attachment_map = build_attachment_mapping_from_data(response.json())
        logger.info(f"Found {len(attachment_map)} attachments in JSON")

        def _process(conn):
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # url gives us the attachment ID which we can use to find the Discord user, and sha1 gets level in db
            rows = cur.execute(
                "SELECT sha1, url FROM combined WHERE source = 'yeoldesheet'"
            ).fetchall()

            updated = skipped_no_att = skipped_not_found = skipped_no_level = not_steward = already_correct = 0

            for row in rows:
                sha1 = row['sha1']
                url = row['url']

                attachment_id = extract_attachment_id(url)
                if not attachment_id:
                    logger.warning(f"No attachment ID in URL: {url}")
                    skipped_no_att += 1
                    continue

                if attachment_id not in attachment_map:
                    logger.warning(f"Attachment {attachment_id} not in JSON (url: {url})")
                    skipped_not_found += 1
                    continue

                discord_user_id, display_name = attachment_map[attachment_id]

                # nb: if level does not exist, do not recreate it, could have been deleted already.
                try:
                    level = RDLevel.objects.get(sha1=sha1)
                except RDLevel.DoesNotExist:
                    skipped_no_level += 1
                    continue

                steward_user = User.objects.get(id="usteward")

                if level.submitter != steward_user:
                    logger.warning(
                        f"Level {level.id} ({level.song!r}) has submitter {level.submitter_id} "
                        f"instead of steward, skipping (url: {url})"
                    )
                    not_steward += 1
                    continue

                user = get_or_create_discord_user(discord_user_id, display_name)

                if level.submitter_id == user.id:
                    already_correct += 1
                    continue

                logger.info(
                    f"{'[DRY RUN] ' if dry_run else ''}"
                    f"Level {level.id} ({level.song!r}): "
                    f"{level.submitter_id} → {user.id} (discord:{discord_user_id} {display_name!r})"
                )

                if not dry_run:
                    level.submitter = user
                    level.save()
                updated += 1

            logger.info(
                f"Done. updated={updated} already_correct={already_correct} "
                f"skipped_no_attachment_id={skipped_no_att} "
                f"skipped_not_in_json={skipped_not_found} "
                f"skipped_level_not_in_db={skipped_no_level} "
                f"skipped_not_steward={not_steward}"
            )

        if db_path:
            conn = sqlite3.connect(db_path)
            try:
                _process(conn)
            finally:
                conn.close()
        else:
            logger.info("Downloading combined.db from API…")
            with NamedTemporaryFile(mode="w+b", suffix=".db") as f:
                f.write(httpx.get(DB_URL).content)
                f.flush()
                conn = sqlite3.connect(f.name)
                try:
                    _process(conn)
                finally:
                    conn.close()