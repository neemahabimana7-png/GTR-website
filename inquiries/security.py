"""Database-backed counters work across workers; raw client IPs are not stored."""
import time
from datetime import datetime, timezone
from django.db.models import F
from django.utils.crypto import salted_hmac
from .models import RateLimitBucket


def take_slot(request, scope, limit, window):
    now = int(time.time())
    period = now // window
    # Forwarded IP headers are deliberately ignored: accepting spoofed values bypasses limits.
    client = request.META.get('REMOTE_ADDR', 'unknown')
    key = salted_hmac('grittech.throttle', f'{scope}:{client}:{period}').hexdigest()
    bucket, _ = RateLimitBucket.objects.get_or_create(
        key=key, defaults={'expires_at': datetime.fromtimestamp((period + 1) * window, timezone.utc)},
    )
    RateLimitBucket.objects.filter(pk=bucket.pk).update(attempts=F('attempts') + 1)
    bucket.refresh_from_db(fields=['attempts'])
    return bucket.attempts <= limit, max(1, window - now % window)
