from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Just say hello world!"

    def handle(self, *args, **options):
        name = None
        if args: name = " ".join(args)
        if name:
            self.stdout.write(f"Hello {name}!")
        else:
            self.stdout.write("Hello World!")

    def add_arguments(self, parser):
        parser.add_argument('args', nargs="*", default ="")