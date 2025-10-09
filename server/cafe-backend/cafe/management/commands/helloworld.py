from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    A simple test command that prints Hello World with optional customization
    """
    help = "Prints Hello World with optional name argument"

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='World',
            help='Name to greet (default: World)'
        )
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help='Number of times to print the greeting (default: 1)'
        )
        parser.add_argument(
            '--uppercase',
            action='store_true',
            help='Print the greeting in uppercase'
        )

    def handle(self, *args, **options):
        name = options['name']
        count = options['count']
        uppercase = options['uppercase']
        
        greeting = f"Hello {name}!"
        
        if uppercase:
            greeting = greeting.upper()
        
        for i in range(count):
            if count > 1:
                self.stdout.write(f"{i + 1}. {greeting}")
            else:
                self.stdout.write(greeting)
        
        # Use Django's styled output for success message
        self.stdout.write(
            self.style.SUCCESS(f'Successfully printed greeting {count} time(s)')
        )
