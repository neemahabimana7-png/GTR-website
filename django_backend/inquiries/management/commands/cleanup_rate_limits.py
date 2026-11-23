from django.core.management.base import BaseCommand
from django.utils import timezone
from inquiries.models import RateLimitBucket


class Command(BaseCommand):
    help = 'Delete expired abuse counters; run daily in production.'

    def handle(self, *args, **options):
        count, _ = RateLimitBucket.objects.filter(expires_at__lt=timezone.now()).delete()
        self.stdout.write(f'Deleted {count} expired rate-limit buckets.')
