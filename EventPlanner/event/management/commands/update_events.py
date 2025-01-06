from django.core.management.base import BaseCommand
from event.models import Events
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'custom command for event management and cleaning'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        print("this ran")
        Events.objects.filter(
            event_status='upcoming',
            start_date__isnull=False,
            start_time__isnull=False,
            start_date__lt=now.date()
        ).update(event_status='ongoing')

        Events.objects.filter(
            event_status='ongoing',
            end_date__isnull=False,
            end_time__isnull=False,
            end_date__lt=now.date()
        ).update(event_status='completed')

        deletion_threshold = now - timedelta(hours=24)
        Events.objects.filter(
            event_status='completed',
            end_date__lte=deletion_threshold.date()
        ).delete()