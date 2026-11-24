"""The only business table stores inquiries; a small expiring table limits abuse."""
from django.db import models
from django.core.validators import MaxLengthValidator


class Inquiry(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In progress'
        CLOSED = 'closed', 'Closed'
        SPAM = 'spam', 'Spam'

    class Notification(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SENDING = 'sending', 'Sending'
        SENT = 'sent', 'Sent'
        FAILED = 'failed', 'Failed'

    submission_id = models.UUIDField(unique=True, editable=False)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField(validators=[MaxLengthValidator(5000)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification_status = models.CharField(max_length=10, choices=Notification.choices, default=Notification.PENDING)
    notification_attempts = models.PositiveIntegerField(default=0)
    notification_sent_at = models.DateTimeField(null=True, blank=True)
    notification_attempted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Inquiry #{self.pk}: {self.subject}'


class RateLimitBucket(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    attempts = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(db_index=True)
