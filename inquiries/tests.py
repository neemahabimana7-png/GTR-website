import time
import uuid
from unittest.mock import patch
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core import mail, signing
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from .forms import InquiryForm, new_submission_token, TOKEN_SALT
from .models import Inquiry, RateLimitBucket
from .services import notify_inquiry


@override_settings(CONTACT_MIN_SECONDS=0, EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', CONTACT_RECIPIENTS=['review@example.test'])
class InquiryTests(TestCase):
    def payload(self, **changes):
        result = {'full_name': 'Test Visitor', 'email': 'visitor@example.test', 'phone': '+250 700 000 000',
                  'company': 'Test organization', 'subject': 'Mineral inquiry', 'message': 'Please discuss our mineral requirements.',
                  'submission_token': new_submission_token(), 'website_url': ''}
        result.update(changes)
        return result

    def submit(self, payload=None):
        with self.captureOnCommitCallbacks(execute=True):
            return self.client.post(reverse('inquiries:contact'), payload or self.payload())

    def make_inquiry(self, **changes):
        data = {name: self.payload()[name] for name in InquiryForm.Meta.fields}
        data.update(changes)
        return Inquiry.objects.create(submission_id=uuid.uuid4(), **data)

    def test_valid_submission_saved_and_email_sent(self):
        response = self.submit()
        self.assertEqual(response.status_code, 302)
        inquiry = Inquiry.objects.get()
        self.assertEqual(inquiry.status, 'new')
        self.assertEqual(inquiry.notification_status, 'sent')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ['visitor@example.test'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_success_message_after_redirect(self):
        response = self.submit()
        self.assertContains(self.client.get(response.url), 'Your message has been received')

    def test_missing_required_fields_rejected(self):
        for field in ['full_name', 'email', 'subject', 'message']:
            with self.subTest(field=field):
                self.assertFalse(InquiryForm(self.payload(**{field: ''})).is_valid())

    def test_optional_phone_and_company(self):
        self.assertTrue(InquiryForm(self.payload(phone='', company='')).is_valid())

    def test_invalid_email_and_long_message(self):
        self.assertFalse(InquiryForm(self.payload(email='invalid')).is_valid())
        self.assertFalse(InquiryForm(self.payload(message='x' * 5001)).is_valid())

    def test_header_injection_rejected(self):
        self.assertFalse(InquiryForm(self.payload(subject='Hello\nBcc: bad@example.test')).is_valid())

    def test_invalid_submission_shows_errors_and_preserves_input(self):
        response = self.submit(self.payload(email='not-valid'))
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Test Visitor', status_code=400)
        self.assertFalse(Inquiry.objects.exists())

    def test_honeypot_blocks_submission(self):
        self.assertEqual(self.submit(self.payload(website_url='spam')).status_code, 400)
        self.assertFalse(Inquiry.objects.exists())

    @override_settings(CONTACT_MIN_SECONDS=2)
    def test_too_fast_submission_rejected(self):
        self.assertFalse(InquiryForm(self.payload()).is_valid())

    def test_tampered_token_rejected(self):
        self.assertFalse(InquiryForm(self.payload(submission_token='tampered')).is_valid())

    def test_token_expiration(self):
        token = new_submission_token()
        with patch('django.core.signing.time.time', return_value=time.time() + 4000):
            self.assertFalse(InquiryForm(self.payload(submission_token=token)).is_valid())

    def test_duplicate_submission_is_idempotent(self):
        data = self.payload()
        self.submit(data)
        self.submit(data)
        self.assertEqual(Inquiry.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(CONTACT_RATE_LIMIT=2)
    def test_contact_rate_limit(self):
        self.submit()
        self.submit()
        response = self.submit()
        self.assertEqual(response.status_code, 429)
        self.assertIn('Retry-After', response)
        self.assertEqual(Inquiry.objects.count(), 2)

    def test_bucket_does_not_store_raw_ip(self):
        self.submit()
        self.assertNotIn('127.0.0.1', RateLimitBucket.objects.get().key)

    def test_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse('inquiries:contact'), self.payload()).status_code, 403)
        client.get(reverse('inquiries:contact'))
        with self.captureOnCommitCallbacks(execute=True):
            response = client.post(reverse('inquiries:contact'), self.payload(), HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value)
        self.assertEqual(response.status_code, 302)

    def test_visitor_html_is_escaped_on_error(self):
        response = self.submit(self.payload(full_name='<script>alert(1)</script>', email='bad'))
        self.assertNotContains(response, '<script>alert(1)</script>', status_code=400)
        self.assertContains(response, '&lt;script&gt;', status_code=400)

    @patch('inquiries.services.EmailMessage.send', side_effect=RuntimeError('SMTP unavailable'))
    def test_email_failure_never_loses_inquiry(self, send):
        self.assertEqual(self.submit().status_code, 302)
        inquiry = Inquiry.objects.get()
        self.assertEqual(inquiry.notification_status, 'failed')
        self.assertEqual(inquiry.notification_attempts, 1)

    def test_failed_notification_can_be_retried(self):
        inquiry = self.make_inquiry(notification_status='failed')
        self.assertTrue(notify_inquiry(inquiry.pk))
        self.assertFalse(notify_inquiry(inquiry.pk))
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(CONTACT_RECIPIENTS=[])
    def test_unconfigured_notification_is_marked_failed(self):
        inquiry = self.make_inquiry()
        self.assertFalse(notify_inquiry(inquiry.pk))
        inquiry.refresh_from_db()
        self.assertEqual(inquiry.notification_status, 'failed')

    @override_settings(ADMIN_LOGIN_RATE_LIMIT=2)
    def test_admin_login_is_rate_limited(self):
        url = reverse('admin:login')
        self.client.post(url, {'username': 'nobody', 'password': 'wrong'})
        self.client.post(url, {'username': 'nobody', 'password': 'wrong'})
        self.assertEqual(self.client.post(url, {}).status_code, 429)

    def test_anonymous_admin_redirects_to_login(self):
        self.assertEqual(self.client.get('/admin/').status_code, 302)

    def test_non_staff_cannot_open_admin(self):
        user = get_user_model().objects.create_user('visitor', password='test-pass-9284')
        self.client.force_login(user)
        self.assertEqual(self.client.get('/admin/').status_code, 302)

    def test_staff_requires_model_permission(self):
        user = get_user_model().objects.create_user('staff', password='test-pass-9284', is_staff=True)
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('admin:inquiries_inquiry_changelist')).status_code, 403)
        user.user_permissions.add(Permission.objects.get(codename='view_inquiry'))
        self.assertEqual(self.client.get(reverse('admin:inquiries_inquiry_changelist')).status_code, 200)

    def test_admin_edit_keeps_original_visitor_message_read_only(self):
        user = get_user_model().objects.create_superuser('admin', 'admin@example.test', 'test-pass-9284')
        self.client.force_login(user)
        inquiry = self.make_inquiry()
        response = self.client.get(reverse('admin:inquiries_inquiry_change', args=[inquiry.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="message"')
        self.assertContains(response, 'name="internal_notes"')

    def test_management_cleanup(self):
        from datetime import timedelta
        from django.core.management import call_command
        from django.utils import timezone
        RateLimitBucket.objects.create(key='expired', expires_at=timezone.now()-timedelta(hours=1))
        call_command('cleanup_rate_limits')
        self.assertFalse(RateLimitBucket.objects.exists())
