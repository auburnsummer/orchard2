from django.core.management.base import BaseCommand
import meilisearch
import time
from orchard.settings import MEILI_API_KEY, MEILI_API_URL

RDLEVEL_INDEX_NAME = "rdlevels"

def get_healthy_client(max_retries=5, retry_delay=2):
    """
    Get a healthy MeiliSearch client, retrying if necessary.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay in seconds between retries
        
    Returns:
        meilisearch.Client: A healthy MeiliSearch client
        
    Raises:
        Exception: If MeiliSearch doesn't become healthy after maximum retries
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
            client.create_index(
                RDLEVEL_INDEX_NAME,
                {
                    "primaryKey": "id"
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully created MeiliSearch index: {RDLEVEL_INDEX_NAME}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error setting up MeiliSearch: {str(e)}")) 