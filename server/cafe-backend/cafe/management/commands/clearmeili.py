from django.core.management import BaseCommand

from cafe.management.commands.setupmeili import get_healthy_client, RDLEVEL_INDEX_NAME

class Command(BaseCommand):
    help = "clear the meilisearch index"
    def handle(self, *args, **options):
        client = get_healthy_client()
        index = client.get_index(RDLEVEL_INDEX_NAME)
        index.delete_all_documents()
