"""Fail closed: this file cannot silently use development credentials or SQLite."""
import os
from .base import *  # noqa: F403
from config.environment import required, csv, boolean
from django.core.exceptions import ImproperlyConfigured

DEBUG = False
SECRET_KEY = required('SECRET_KEY')
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured('Use a unique production SECRET_KEY of at least 50 characters.')
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}
ALLOWED_HOSTS = csv('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = csv('CSRF_TRUSTED_ORIGINS')
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured('Explicit production ALLOWED_HOSTS are required.')
DB_ENGINE = os.environ.get('DB_ENGINE', 'postgresql').strip().lower()
if DB_ENGINE == 'sqlite':
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('SQLITE_PATH', '/data/db.sqlite3'),
        'OPTIONS': {'timeout': 20},
    }}
elif DB_ENGINE == 'postgresql':
    DATABASES = {'default': {
        'ENGINE': 'django.db.backends.postgresql', 'NAME': required('DB_NAME'),
        'USER': required('DB_USER'), 'PASSWORD': required('DB_PASSWORD'),
        'HOST': required('DB_HOST'), 'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60, 'OPTIONS': {'sslmode': os.environ.get('DB_SSLMODE', 'verify-full')},
    }}
else:
    raise ImproperlyConfigured('DB_ENGINE must be sqlite or postgresql.')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = required('EMAIL_HOST')
DEFAULT_FROM_EMAIL = required('DEFAULT_FROM_EMAIL')
CONTACT_RECIPIENTS = csv('CONTACT_RECIPIENTS')
if not CONTACT_RECIPIENTS:
    raise ImproperlyConfigured('CONTACT_RECIPIENTS is required.')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
# Enable only behind a proxy that overwrites untrusted incoming forwarding headers.
if boolean('TRUST_HTTPS_PROXY', False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
