from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from inquiries.models import Inquiry
from inquiries.services import notify_inquiry


class Command(BaseCommand):
    help = 'Retry unsent notifications. A crash-recovery retry may deliver a duplicate email.'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=20)
        parser.add_argument('--recover-stale', action='store_true', help='Reset sending attempts older than 15 minutes.')

    def handle(self, *args, **options):
        if options['recover_stale']:
            Inquiry.objects.filter(notification_status='sending', notification_attempted_at__lt=timezone.now()-timedelta(minutes=15)).update(notification_status='failed')
        ids = list(Inquiry.objects.filter(notification_status__in=['pending', 'failed']).values_list('pk', flat=True)[:max(0, options['limit'])])
        count = sum(notify_inquiry(pk) for pk in ids)
        self.stdout.write(f'{count} of {len(ids)} notifications accepted by the email backend.')
