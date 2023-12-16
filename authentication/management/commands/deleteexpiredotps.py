from django.utils import timezone
from authentication.models import Otp
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "delete all the expired tokens used for account verifications"

    def handle(self, *args, **options):
        """entry point of the command"""
        try:
            self.stdout.write('Deleting all otp entries')
            five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
            Otp.objects.filter(date_created__lte=five_minutes_ago).delete()
            self.stdout.write(self.style.SUCCESS('Complete'))
        except Exception as e:
            self.stderr.write(e)
