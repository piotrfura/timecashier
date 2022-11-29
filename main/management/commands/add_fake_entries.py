from django.core.management.base import BaseCommand

from entries.utils import create_entries


class Command(BaseCommand):
    help = "Create [-n] fake entries, default 10"

    def handle(self, *args, **options):
        n = options.get("number", 10)
        create_entries(n)
        self.stdout.write(f'{n} entries has been created')

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int, default=10, dest="number", help="Amount of entries")
