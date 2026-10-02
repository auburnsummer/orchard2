import json
from django.core.management.base import BaseCommand
import typesense
from cafe.management.commands.setuptypesense import RDLEVEL_ALIAS_NAME, get_typesense_client, client_healthy
from cafe.models import RDLevel
from cafe.tasks.sync_level_to_typesense import mass_sync_levels_to_typesense

class Command(BaseCommand):
    help = "Clear Typesense collection"

    def handle(self, *args, **options):
        self.stdout.write("Clearing Typesense collection...")
        typesense_client = get_typesense_client()

        if not client_healthy(typesense_client):
            print("Typesense is not healthy. Exiting mass sync.")
            return
    
        typesense_client.collections[RDLEVEL_ALIAS_NAME].delete()