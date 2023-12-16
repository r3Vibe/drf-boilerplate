from authentication.models import Tokens
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "delete all the expired tokens used for account verifications"

    def handle(self, *args, **options):
        """entry point of the command"""
        try:
            self.stdout.write('Deleting all token entries')
            Tokens.objects.filter(is_valid=False).delete()
            self.stdout.write(self.style.SUCCESS('Complete'))
        except Exception as e:
            self.stderr.write(e)
