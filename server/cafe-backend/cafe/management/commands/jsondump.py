import json

from django.core.management.base import BaseCommand

from cafe.models.rdlevels.rdlevel import RDLevel


class Command(BaseCommand):
    """
    Dumps the RDLevel table to a JSONL file.
    """
    help = "Dumps RDLevel table to JSONL file"

    def add_arguments(self, parser):
        parser.add_argument(
            '--filename',
            type=str,
            default='rdlevels-dump.jsonl',
            help='Filename for the dump (default: rdlevels-dump.jsonl)'
        )

    def handle(self, *args, **options):
        filename = options['filename']
        
        self.stdout.write(f"Starting JSONL dump of rdlevels...")
        
        # private levels are not in the dump
        levels = RDLevel.objects.filter(is_private=False)
        
        total_count = levels.count()
        self.stdout.write(f"Found {total_count} levels to export")

        with open(filename, 'wb') as f:
            for level in levels.iterator():
                level_dict = level.to_dict()
                json_line = json.dumps(level_dict, ensure_ascii=False)
                f.write(json_line.encode('utf-8') + b'\n')
        
        self.stdout.write(self.style.SUCCESS(f"Successfully dumped {total_count} levels to {filename}"))