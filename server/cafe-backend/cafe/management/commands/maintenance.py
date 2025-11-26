from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    """
    Toggle maintenance mode by creating/removing /app/maintenance.on file
    """
    help = "Turn maintenance mode on or off"
    
    MAINTENANCE_FILE = Path("/app/maintenance.on")

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=['on', 'off', 'status'],
            help='Action to perform: on, off, or status'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'status':
            self._show_status()
        elif action == 'on':
            self._turn_on()
        elif action == 'off':
            self._turn_off()

    def _show_status(self):
        """Show current maintenance mode status"""
        if self.MAINTENANCE_FILE.exists():
            self.stdout.write(
                self.style.WARNING('Maintenance mode is ON')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Maintenance mode is OFF')
            )

    def _turn_on(self):
        """Turn on maintenance mode"""
        if self.MAINTENANCE_FILE.exists():
            self.stdout.write(
                self.style.WARNING('Maintenance mode is already ON')
            )
            return
        
        try:
            # Create parent directory if it doesn't exist
            self.MAINTENANCE_FILE.parent.mkdir(parents=True, exist_ok=True)
            # Create the maintenance file
            self.MAINTENANCE_FILE.touch()
            self.stdout.write(
                self.style.SUCCESS('✓ Maintenance mode turned ON')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to turn on maintenance mode: {e}')
            )

    def _turn_off(self):
        """Turn off maintenance mode"""
        if not self.MAINTENANCE_FILE.exists():
            self.stdout.write(
                self.style.WARNING('Maintenance mode is already OFF')
            )
            return
        
        try:
            self.MAINTENANCE_FILE.unlink()
            self.stdout.write(
                self.style.SUCCESS('✓ Maintenance mode turned OFF')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to turn off maintenance mode: {e}')
            )
