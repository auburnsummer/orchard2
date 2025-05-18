import meilisearch

from django.core.management.base import BaseCommand

from orchard.settings import MEILI_API_KEY, MEILI_API_URL

RDLEVEL_INDEX_NAME = "rdlevels"

client = meilisearch.Client(MEILI_API_URL, MEILI_API_KEY)

class Command(BaseCommand):
    help = "set up the meilisearch indexes"
    def handle(self, *args, **options):
        client.create_index(
            RDLEVEL_INDEX_NAME,
            {
                "primaryKey": "id"
            }
        )
        print("Index created")
