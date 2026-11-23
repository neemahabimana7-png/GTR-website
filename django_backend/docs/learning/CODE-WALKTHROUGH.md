# Important Python files: actual implementation walkthrough

Read a file with its matching lesson. The excerpts below come directly from the implemented code, not unrelated examples. Empty package __init__.py files contain no business logic.

## `manage.py` — Command entry point

Sets a safe local settings default and hands terminal arguments to Django. It does not contain website business logic.

```python
#!/usr/bin/env python
"""Run Django management commands from this isolated backend directory."""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
```

## `config/environment.py` — Environment helpers

load_environment reads literal private configuration without executing shell text. boolean/csv parse settings; required refuses absent production values.

```python
def load_environment(path):
    if not Path(path).is_file():
        return
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, separator, value = line.partition('=')
        if not separator or not key.strip().replace('_', '').isalnum():
            raise ImproperlyConfigured('Invalid .env assignment; use NAME=value.')
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
```

## `config/settings/base.py` — Shared settings

Connects apps, middleware, template lookup, static directories and common security limits. Middleware order keeps sessions/auth/CSRF available for views and staff handling.

```python
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'website', 'inquiries',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'inquiries.middleware.AdminLoginThrottleMiddleware',
```

## `config/settings/development.py` — Local settings

Creates/reuses a private random local secret, selects SQLite and console email, and restricts allowed local hosts. No live company credentials are invented.

```python
DEBUG = True
ALLOWED_HOSTS = csv('ALLOWED_HOSTS', 'localhost,127.0.0.1,[::1],testserver')
local = BASE_DIR / '.local'
local.mkdir(exist_ok=True)
secret_path = local / 'development-secret'
if not secret_path.exists():
    try:
        with secret_path.open('x', encoding='utf-8') as handle:
            handle.write(secrets.token_urlsafe(64))
    except FileExistsError:
        pass
SECRET_KEY = os.environ.get('SECRET_KEY') or secret_path.read_text().strip()
```

## `config/settings/production.py` — Production settings

Requires secrets, explicit hosts, PostgreSQL and SMTP information; enables secure cookies/HTTPS. It imports shared settings and overrides development-sensitive behavior.

```python
DEBUG = False
SECRET_KEY = required('SECRET_KEY')
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured('Use a unique production SECRET_KEY of at least 50 characters.')
ALLOWED_HOSTS = csv('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = csv('CSRF_TRUSTED_ORIGINS')
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured('Explicit production ALLOWED_HOSTS are required.')
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql', 'NAME': required('DB_NAME'),
    'USER': required('DB_USER'), 'PASSWORD': required('DB_PASSWORD'),
    'HOST': required('DB_HOST'), 'PORT': os.environ.get('DB_PORT', '5432'),
```

## `config/urls.py` — Top-level routing

Delegates /admin/, public routes and /contact/ to their owners. include() composes URL modules rather than mixing all view code here.

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('contact/', include('inquiries.urls')),
]
```

## `config/wsgi.py` — WSGI entry point

Exposes application to a production WSGI server. It defaults to production settings; Waitress imports this object.

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()
```

## `config/asgi.py` — ASGI entry point

Provides the equivalent asynchronous server entry point if an ASGI hosting service is selected later. No websocket feature is added.

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_asgi_application()
```

## `website/pages.py` — Public-page registry

PAGES maps route names to explicit URL paths and original HTML filenames. Both partnership variants remain separate records in this Python mapping, not database rows.

```python
PAGES = {
    'home': ('', 'grittech.html'),
    'about': ('about/', 'about.html'),
    'services': ('services/', 'services/service.html'),
    'sourcing': ('services/gold-3t-mineral-sourcing/', 'services/services-details-mineralTrading/serviceMineralTrading.html'),
    'trading': ('services/mineral-trading/', 'services/services-details-export/service-details-export.html'),
    'supply': ('services/mineral-supply-chain/', 'services/services-details-supply/services-details-supply.html'),
    'quality': ('services/mineral-quality-grade-management/', 'services/services-details-quality/services-details-quality.html'),
    'traceability': ('services/mineral-traceability-compliance/', 'services/services-details-traceability/services-details-traceability.html'),
    'markets': ('services/international-market-access/', 'services/services-details-globalmarket/services-details-globalmark.html'),
    'partnerships': ('services/strategic-partnerships/', 'services/services-details-parternship/services-details-partner.html'),
    'partnerships-alternative': ('services/strategic-partnerships/alternative/', 'services/services-details-/services-details-partner.html'),
```

## `website/urls.py` — Public and legacy routes

Builds named routes and RedirectView aliases from the registry. Old HTML bookmarks keep working through redirects; unknown paths are not accepted as filenames.

```python
urlpatterns = []
for name, (route, source) in PAGES.items():
    urlpatterns.append(path(route, views.page, {'page_key': name}, name=name))
    urlpatterns.append(path(source, RedirectView.as_view(pattern_name='website:' + name, permanent=True)))
urlpatterns.append(path('contact.html', RedirectView.as_view(pattern_name='inquiries:contact', permanent=True)))
```

## `website/views.py` — Marketing page view

page() uses require_safe to accept only GET/HEAD and render the allowlisted copied template. No unnecessary database query occurs.

```python
def page(request, page_key):
    return render(request, 'pages/' + PAGES[page_key][1])
```

## `inquiries/models.py` — Persistent records

Inquiry stores visitor data, workflow and notification state; TextChoices gives readable statuses. RateLimitBucket stores only expiring hashed counters. Meta orders messages newest first.

```python
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
```

## `inquiries/forms.py` — Input boundary

new_submission_token signs a UUID/start time. InquiryForm reuses approved model fields, rejects header newlines and validates timing/signature/honeypot in clean(). cleaned_data, not raw POST, flows into the view save.

```python
def new_submission_token():
    return signing.dumps({'id': str(uuid.uuid4()), 'started': time.time()}, salt=TOKEN_SALT)


class InquiryForm(forms.ModelForm):
    submission_token = forms.CharField(widget=forms.HiddenInput)
    website_url = forms.CharField(required=False)  # Honeypot; genuine visitors leave it empty.

    class Meta:
        model = Inquiry
        fields = ['full_name', 'email', 'phone', 'company', 'subject', 'message']

```

## `inquiries/views.py` — Contact workflow

contact() creates blank GET forms, rate-limits POST, validates, atomically saves a unique submission and registers email after commit. Invalid data is returned with the same bound fields; success uses a redirect/message.

```python
def contact(request):
    status = 200
    form = InquiryForm(initial={'submission_token': new_submission_token()})
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        allowed, retry = take_slot(request, 'contact', settings.CONTACT_RATE_LIMIT, settings.CONTACT_RATE_WINDOW)
        if not allowed:
            form.is_valid()
            form.add_error(None, 'Too many submissions. Please wait a few minutes before trying again.')
            response = render(request, 'pages/contact.html', {'form': form}, status=429)
            response['Retry-After'] = str(retry)
            return response
```

## `inquiries/urls.py` — Contact route

Names the single contact endpoint so templates and redirects use inquiries:contact rather than relative filenames.

```python
urlpatterns = [path('', contact, name='contact')]
```

## `inquiries/security.py` — Shared abuse counter

take_slot derives an HMAC key from scope/client/window, increments with an F expression and returns allowed/retry seconds. The database provides shared state across workers; raw IP is not stored.

```python
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
```

## `inquiries/middleware.py` — Admin login boundary

AdminLoginThrottleMiddleware intercepts login POST attempts before reaching the admin view and returns HTTP 429 after the configured limit. It does not replace Django authentication.

```python
class AdminLoginThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == reverse('admin:login'):
            allowed, retry = take_slot(request, 'admin-login', settings.ADMIN_LOGIN_RATE_LIMIT, settings.ADMIN_LOGIN_RATE_WINDOW)
            if not allowed:
                response = HttpResponse('Too many login attempts. Please try again later.', status=429)
                response['Retry-After'] = str(retry)
                return response
        return self.get_response(request)
```

## `inquiries/services.py` — Notification service

notify_inquiry atomically claims an unsent record, renders the email template and uses a company From plus visitor Reply-To. Failure marks failed without losing the inquiry. Sent records cannot be resent by ordinary retry.

```python
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
```

## `inquiries/admin.py` — Staff interface

InquiryAdmin defines list/search/filter/read-only behavior and a change-permission retry action. Original visitor fields are protected from accidental staff edits.

```python
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

```

## `inquiries/migrations/0001_initial.py` — Initial schema

Generated by Django from actual model definitions. Creates Inquiry and RateLimitBucket. Run migrate to apply; do not edit an applied production migration casually.

```python
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
```

## `inquiries/management/commands/cleanup_rate_limits.py` — Expiry maintenance

Command deletes expired counter rows using timezone-aware comparisons. It is safe for inquiries because it only queries RateLimitBucket.

```python
class Command(BaseCommand):
    help = 'Delete expired abuse counters; run daily in production.'

    def handle(self, *args, **options):
        count, _ = RateLimitBucket.objects.filter(expires_at__lt=timezone.now()).delete()
        self.stdout.write(f'Deleted {count} expired rate-limit buckets.')
```

## `inquiries/management/commands/retry_notifications.py` — Notification maintenance

Command retries unsent records in bounded batches. Optional stale recovery resets interrupted sends older than 15 minutes, with an explicit duplicate-email caveat.

```python
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
```

## `website/tests.py` — Page/preservation tests

Uses Django SimpleTestCase for page requests, named/legacy URLs, local assets and hash comparisons. It does not test third-party CDN servers.

```python
class PageIntegrationTests(SimpleTestCase):
    def test_every_public_page_renders(self):
        # Contact uses the database only on POST, so it can be checked here too.
        for name in PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse('website:' + name))
                self.assertEqual(response.status_code, 200)
                self.assertNotIn(b'{%', response.content)

    def test_contact_renders(self):
        self.assertEqual(self.client.get(reverse('inquiries:contact')).status_code, 200)

```

## `inquiries/tests.py` — Business/security tests

Uses isolated TestCase databases, locmem email and mocks to prove success/failure/abuse/admin behavior without sending internet email. captureOnCommitCallbacks runs deferred email work in tests.

```python
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

```

## `scripts/verify_frontend.py` — Whole-frontend evidence

Compares baseline SHA-256 hashes, copied assets, normalized original/rendered DOM tokens and inline scripts. Only technical URL/form bindings are normalized; visible content/classes remain comparable.

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
import django
django.setup()
from django.test import Client
from django.urls import reverse
from website.pages import PAGES

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
ROUTES = {source: reverse('website:' + name) for name, (_, source) in PAGES.items()}
ROUTES['contact.html'] = reverse('inquiries:contact')
ROUTES['services/services-details-quality/services-details-supply.html'] = reverse('website:supply')

```

## Follow one real data flow

`/contact/` -> config.urls -> inquiries.urls -> contact() -> take_slot() -> InquiryForm.is_valid() -> cleaned_data -> Inquiry.get_or_create() -> transaction commit -> notify_inquiry() -> emails/inquiry.txt -> redirect -> feedback include. Later InquiryAdmin reads the same row. CSS/JavaScript do not participate in the database save.
