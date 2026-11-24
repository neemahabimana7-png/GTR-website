"""Small, explicit .env reader: no shell execution or secret interpolation."""
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured


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
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def boolean(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    if value.lower() not in {'true', 'false', '1', '0'}:
        raise ImproperlyConfigured(f'{name} must be true or false.')
    return value.lower() in {'true', '1'}


def csv(name, default=''):
    return [item.strip() for item in os.environ.get(name, default).split(',') if item.strip()]


def required(name):
    value = os.environ.get(name, '').strip()
    if not value:
        raise ImproperlyConfigured(f'{name} is required for production.')
    return value
