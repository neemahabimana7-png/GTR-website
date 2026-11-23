"""Sending is separate from saving: email failure must never lose an inquiry."""
import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import F
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Inquiry

logger = logging.getLogger(__name__)


def notify_inquiry(inquiry_id):
    # Claim the attempt atomically so two staff retry actions cannot both send it.
    claimed = Inquiry.objects.filter(
        pk=inquiry_id, notification_status__in=[Inquiry.Notification.PENDING, Inquiry.Notification.FAILED],
    ).update(notification_status=Inquiry.Notification.SENDING,
             notification_attempts=F('notification_attempts') + 1, notification_attempted_at=timezone.now())
    if not claimed:
        return False
    inquiry = Inquiry.objects.get(pk=inquiry_id)
    try:
        if not settings.CONTACT_RECIPIENTS:
            raise ValueError('Notification recipients not configured')
        email = EmailMessage(
            subject=f'Website inquiry #{inquiry.pk}: {inquiry.subject}',
            body=render_to_string('emails/inquiry.txt', {'inquiry': inquiry}),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.CONTACT_RECIPIENTS, reply_to=[inquiry.email],
        )
        if email.send(fail_silently=False) != 1:
            raise RuntimeError('Email backend did not accept the message')
    except Exception:
        Inquiry.objects.filter(pk=inquiry_id).update(notification_status=Inquiry.Notification.FAILED)
        # Do not log SMTP secrets, inquiry text, or email addresses.
        logger.warning('Notification failed for inquiry %s; retained for staff retry.', inquiry_id)
        return False
    Inquiry.objects.filter(pk=inquiry_id).update(
        notification_status=Inquiry.Notification.SENT, notification_sent_at=timezone.now())
    return True
