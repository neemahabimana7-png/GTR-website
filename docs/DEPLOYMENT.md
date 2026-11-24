# Production deployment preparation — not deployed

No public deployment, domain change, server creation or live email delivery was performed. Deployment requires explicit authorization and actual hosting/domain/email decisions.

## Install and configure

Create a fresh environment on the target host. Install `requirements/production.txt` (Django, Psycopg PostgreSQL driver and Waitress). Keep production secrets in the host's secret manager or a private `.env`. Choose `config.settings.production` in the process environment or command; do not select it from `.env`.

Required configuration:

- `SECRET_KEY`: unique random private value, at least 50 characters. Generate locally; never paste it into documentation or source control.
- `ALLOWED_HOSTS`: actual approved hostnames, comma-separated; no wildcard.
- `CSRF_TRUSTED_ORIGINS`: HTTPS origins when required by the deployed origin/proxy arrangement.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, optional `DB_PORT`.
- `DB_SSLMODE`: defaults to `verify-full`. Install the provider's CA or configure its certificate requirements. Any weaker mode requires an explicit infrastructure decision.
- `EMAIL_HOST`, port/TLS/SSL, provider username/password when needed.
- `DEFAULT_FROM_EMAIL`: approved verified sender. `CONTACT_RECIPIENTS`: approved company recipients.
- `TRUST_HTTPS_PROXY=true` only behind a trusted HTTPS-terminating proxy.

```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.production"
.\.venv\Scripts\python.exe manage.py check --deploy
.\.venv\Scripts\python.exe manage.py migrate --noinput
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8000 config.wsgi:application
```

These are commands for an authorized deployment, not commands already executed against production. The production settings deliberately fail if essential values are absent. WSGI defaults to production; never run development settings on a public production server.

## Infrastructure responsibilities

Place an HTTPS reverse proxy in front of Waitress. Serve `/static/` from `static_collected/`, including Django Admin assets. Production `runserver` static serving is not used. Forward traffic only from trusted infrastructure and configure the server to replace client/protocol headers; the app ignores arbitrary forwarded IPs. Apply upstream body limits, login/contact rate limits, logging controls and access restrictions. Choose a single authenticated proxy configuration specific to the host rather than copying a wildcard trust setting.

Use a restricted PostgreSQL application role and private connectivity. Configure provider backups and monitoring. Run tests on PostgreSQL in staging; local SQLite tests do not establish production concurrency or database compatibility. Validate email through a staging mailbox, including failure and retry behavior, before opening the contact form publicly.

## Release checklist

1. Approve the domain, host, recipient, sender, administrators and inquiry retention period.
2. Back up the database and current release.
3. Install pinned dependencies in an isolated environment; review updates.
4. Run automated tests and frontend verification against the agreed baseline.
5. Apply migrations and collect static files.
6. Run production deployment checks and test HTTPS, admin access, static files and contact submission.
7. Schedule `cleanup_rate_limits` daily and monitored notification retry if desired; commands are included, no OS schedule was created.
8. Verify rollback and restoration procedures. Roll code back only with database-compatible migrations; do not delete real inquiries.

The repository keeps frontend source for reference. The web server must expose only Django routes and collected static files, never `.env`, `.local`, the full project tree, backup archives or Git metadata.
