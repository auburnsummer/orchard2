from django.core.management import BaseCommand

from cafe.management.commands.setupmeili import client, RDLEVEL_INDEX_NAME

class Command(BaseCommand):
    help = "clear the meilisearch index"
    def handle(self, *args, **options):
        index = client.get_index(RDLEVEL_INDEX_NAME)
        index.delete_all_documents()
