"""Local-only defaults. The generated secret and SQLite file are ignored by Git."""
import os
import secrets
from .base import *  # noqa: F403
from config.environment import csv

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
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': local / 'db.sqlite3', 'OPTIONS': {'timeout': 20}}}
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
# These are explicitly local test sinks, not invented company mailboxes.
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL') or 'development@localhost'
CONTACT_RECIPIENTS = csv('CONTACT_RECIPIENTS', 'local-review@localhost')
