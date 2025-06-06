from django.core.management.base import BaseCommand
import meilisearch
import time
from orchard.settings import MEILI_API_KEY, MEILI_API_URL

RDLEVEL_INDEX_NAME = "rdlevels"

def get_healthy_client(max_retries=5, retry_delay=2):
    """
    Get a healthy MeiliSearch client, retrying if necessary.
    """
    client = meilisearch.Client(MEILI_API_URL, MEILI_API_KEY)
    
    for attempt in range(max_retries):
        if client.is_healthy():
            return client
        if attempt < max_retries - 1:
            print(f"MeiliSearch not ready, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    raise Exception("MeiliSearch failed to become healthy after maximum retries")

class Command(BaseCommand):
    help = "Initialize MeiliSearch index"

    def handle(self, *args, **options):
        try:
            client = get_healthy_client()

            index = client.index(RDLEVEL_INDEX_NAME)
            index.update(primary_key="id")
            index.update_filterable_attributes(
                body=[
                    "artist_tokens",
                    "seizure_warning",
                    "authors",
                    "min_bpm",
                    "max_bpm",
                    "difficulty",
                    "single_player",
                    "two_player",
                    "tags",
                    "has_classics",
                    "has_squareshots",
                    "has_oneshots",
                    "has_freezeshots",
                    "has_freetimes",
                    "has_holds",
                    "has_skipshots",
                    "has_window_dance",
                    "submitter.id",
                    "club.id",
                    "approval",
                ]
            )
            index.update_sortable_attributes(
                body=[
                    "last_updated"
                ]
            )

            self.stdout.write(self.style.SUCCESS(f"Successfully created MeiliSearch index: {RDLEVEL_INDEX_NAME}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error setting up MeiliSearch: {str(e)}")) 