import json
from django.core.management.base import BaseCommand
from cafe.management.commands.setuptypesense import RDLEVEL_ALIAS_NAME, get_typesense_client, client_healthy
from cafe.models import RDLevel
from cafe.tasks.sync_level_to_typesense import mass_sync_levels_to_typesense

class Command(BaseCommand):
    help = "Sync data to Typesense"

    def handle(self, *args, **options):
        self.stdout.write("Syncing data to Typesense...")
        typesense_client = get_typesense_client()

        if not client_healthy(typesense_client):
            print("Typesense is not healthy. Exiting mass sync.")
            return
    
        levels_in_typesense = set()
        for line in typesense_client.collections[RDLEVEL_ALIAS_NAME].documents.export({
            "fields": "id"
        }).splitlines():
            doc = json.loads(line)
            levels_in_typesense.add(doc["id"])

        levels_in_cafe = set()
        for level in RDLevel.objects.all():
            levels_in_cafe.add(level.id)

        levels_to_delete = levels_in_typesense - levels_in_cafe
        levels_to_add = levels_in_cafe - levels_in_typesense

        if levels_to_delete:
            print(f"Deleting {len(levels_to_delete)} levels from Typesense...")
            for level_id in levels_to_delete:
                try:
                    typesense_client.collections[RDLEVEL_ALIAS_NAME].documents[level_id].delete()
                except Exception as e:
                    print(f"Error deleting level {level_id} from Typesense: {e}")

        if levels_to_add:
            mass_sync_levels_to_typesense(levels_to_add)

        print(f"Levels in Typesense: {len(levels_in_typesense)}"
              f", Levels in Cafe: {len(levels_in_cafe)}"
              f", To delete: {len(levels_to_delete)}"
              f", To add: {len(levels_to_add)}")

