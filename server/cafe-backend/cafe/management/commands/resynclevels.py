from django.core.management import BaseCommand

from cafe.models import RDLevel
from cafe.tasks.sync_level_to_meili import sync_level_to_meili


class Command(BaseCommand):
    help = "Sync all levels with meili"

    def handle(self, *args, **options):
        all_levels = RDLevel.objects.all()
        for level in all_levels:
            sync_level_to_meili(level.id)