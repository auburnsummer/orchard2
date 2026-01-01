from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from cafe.models.clubs.club import Club
from cafe.models.rdlevels.rdlevel import RDLevel


class Command(BaseCommand):
    """
    Transfer all rdlevels from one club to another club
    """
    help = "Transfer all rdlevels from one club to another club"

    def add_arguments(self, parser):
        parser.add_argument(
            '--from_club_id',
            type=str,
            help='ID of the club to transfer levels from'
        )
        parser.add_argument(
            '--to_club_id',
            type=str,
            help='ID of the club to transfer levels to'
        )

    def handle(self, *args, **options):
        from_club_id = options['from_club_id']
        to_club_id = options['to_club_id']

        # Validate that the clubs exist
        try:
            from_club = Club.objects.get(id=from_club_id)
        except Club.DoesNotExist:
            raise CommandError(f"Source club '{from_club_id}' does not exist")

        try:
            to_club = Club.objects.get(id=to_club_id)
        except Club.DoesNotExist:
            raise CommandError(f"Destination club '{to_club_id}' does not exist")

        # Get all levels from the source club
        source_levels = RDLevel.objects.filter(club=from_club)
        level_count = source_levels.count()

        # Display information about the transfer
        self.stdout.write(f"\nTransfer Summary:")
        self.stdout.write(f"  From: {from_club.name} ({from_club_id})")
        self.stdout.write(f"  To: {to_club.name} ({to_club_id})")
        self.stdout.write(f"  Levels to transfer: {level_count}")

        try:
            updated_count = 0
            self.stdout.write("\nTransferring levels...")
            # nb: we need to call save() so that typesense syncs.
            # this isn't really a time-sensitive operation, so just do them one at a time.
            for level in source_levels:
                level.club = to_club
                level.save()
                updated_count = updated_count + 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Successfully transferred {updated_count} level(s) from "
                    f"'{from_club.name}' to '{to_club.name}'"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Transferred {updated_count} levels before an error occured"
                )
            )
            raise CommandError(f"Failed to transfer levels: {str(e)}")
