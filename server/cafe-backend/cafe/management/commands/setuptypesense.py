import typesense

from django.core.management.base import BaseCommand

from orchard.settings import TYPESENSE_API_KEY, TYPESENSE_API_HOST, TYPESENSE_API_PORT, TYPESENSE_API_PROTOCOL

import time

RDLEVEL_ALIAS_NAME = "rdlevels"
RDLEVEL_COLLECTION_NAME = "rdlevels1"

typesense_client = typesense.Client({
    'api_key': TYPESENSE_API_KEY,
    'nodes': [{
        'host': TYPESENSE_API_HOST,
        'port': TYPESENSE_API_PORT,
        'protocol': TYPESENSE_API_PROTOCOL
    }],
    'connection_timeout_seconds': 5.0
})

def client_healthy(client: typesense.Client, max_retries=5, retry_delay=2):
    """
    Check if the Typesense client is healthy, retrying if necessary.
    """
    for attempt in range(max_retries):
        try:
            if client.operations.is_healthy():
                return True
        except:
            if attempt < max_retries - 1:
                print(f"Typesense not ready, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception("Typesense failed to become healthy after maximum retries")
    return False

class Command(BaseCommand):
    help = "Initialize Typesense collection"
    
    def handle(self, *args, **options):
        if not client_healthy(typesense_client):
            self.stderr.write("Typesense is not healthy. Exiting setup.")
            return
        
        # Check if the collection already exists
        try:
            coll = typesense_client.collections[RDLEVEL_COLLECTION_NAME].retrieve()
        except typesense.exceptions.ObjectNotFound:
            coll = None
        if not coll:
            self.stdout.write(f"Creating Typesense collection: {RDLEVEL_COLLECTION_NAME}")
            typesense_client.collections.create({
                "name": RDLEVEL_COLLECTION_NAME,
                "enable_nested_fields": True,
                "fields": [
                    {
                        "name": "artist_tokens",
                        "type": "string[]",
                        "facet": True,
                        "infix": True,
                        "locale": "ja"
                    },
                    {
                        "name": "song",
                        "type": "string",
                        "infix": True,
                        "locale": "ja"
                    },
                    {
                        "name": "song_alt",
                        "type": "string",
                        "optional": True,
                        "infix": True,
                        "locale": "ja"
                    },
                    {
                        "name": "seizure_warning",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "description",
                        "type": "string"
                    },
                    {
                        "name": "authors",
                        "type": "string[]",
                        "facet": True,
                        "infix": True,
                        "locale": "ja"
                    },
                    {
                        "name": "max_bpm",
                        "type": "float"
                    },
                    {
                        "name": "min_bpm",
                        "type": "float"
                    },
                    {
                        "name": "difficulty",
                        "type": "int32",
                        "facet": True
                    },
                    {
                        "name": "single_player",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "two_player",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "last_updated",
                        "type": "int64"
                    },
                    {
                        "name": "tags",
                        "type": "string[]",
                        "infix": True,
                        "facet": True,
                        "locale": "ja"
                    },
                    {
                        "name": "has_classics",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "has_oneshots",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "has_squareshots",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "has_freezeshots",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "has_freetimes",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "has_holds",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "has_skipshots",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "has_window_dance",
                        "type": "bool",
                        "facet": True
                    },
                    {
                        "name": "submitter.id",
                        "type": "string",
                        "facet": True
                    },
                    {
                        "name": "club.id",
                        "type": "string",
                        "facet": True
                    },
                    {
                        "name": "approval",
                        "type": "int32"
                    }
                ]
            })
        else:
            self.stdout.write(f"Typesense collection {RDLEVEL_COLLECTION_NAME} already exists.")
        # Create or update the alias
        typesense_client.aliases.upsert(RDLEVEL_ALIAS_NAME, {
            "collection_name": RDLEVEL_COLLECTION_NAME
        })
        self.stdout.write(self.style.SUCCESS(f"Successfully created Typesense collection: {RDLEVEL_COLLECTION_NAME} with alias {RDLEVEL_ALIAS_NAME}"))