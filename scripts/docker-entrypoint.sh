#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec waitress-serve \
    --listen="0.0.0.0:${PORT:-8000}" \
    --trusted-proxy="${WAITRESS_TRUSTED_PROXY:-*}" \
    --trusted-proxy-headers=x-forwarded-proto \
    config.wsgi:application
