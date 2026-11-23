from django.contrib import admin, messages
from .models import Inquiry
from .services import notify_inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'subject', 'status', 'created_at', 'notification_status']
    list_filter = ['status', 'notification_status', 'created_at']
    search_fields = ['full_name', 'email', 'company', 'subject']
    readonly_fields = [
        'submission_id', 'full_name', 'email', 'phone', 'company', 'subject', 'message',
        'created_at', 'updated_at', 'notification_status', 'notification_attempts',
        'notification_sent_at', 'notification_attempted_at',
    ]
    actions = ['retry_notifications']
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False

    @admin.action(description='Retry pending or failed company notifications', permissions=['change'])
    def retry_notifications(self, request, queryset):
        sent = sum(notify_inquiry(pk) for pk in queryset.values_list('pk', flat=True))
        self.message_user(request, f'{sent} notification(s) accepted by the email backend.', messages.INFO)
