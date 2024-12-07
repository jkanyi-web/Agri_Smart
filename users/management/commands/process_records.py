from django.utils import timezone
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from users.models import Crop

class Command(BaseCommand):
    help = 'Process more than 1k records/day'

    def handle(self, *args, **kwargs):
        user = User.objects.filter(username='testuser').first()
        if not user:
            self.stdout.write(self.style.ERROR('User "testuser" not found in the database.'))
            return

        for i in range(1004):
            Crop.objects.create(
                name=f'Crop {i}',
                user=user,
                planting_date=timezone.now(),
                growth_stage='',
                next_activity='',
                next_activity_date=timezone.now()
            )
        self.stdout.write(self.style.SUCCESS('Successfully processed 1k records'))
