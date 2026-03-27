from django.core.management.base import BaseCommand
from parsers.matcher.match_by_mpn import MPNMatcher

class Command(BaseCommand):
    help = 'Match shop items by MPN to reference components'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, help='Limit number of items to match')

    def handle(self, *args, **options):
        matcher = MPNMatcher()
        matched = matcher.run(limit=options.get('limit'))
        self.stdout.write(self.style.SUCCESS(f'Successfully matched {matched} items'))