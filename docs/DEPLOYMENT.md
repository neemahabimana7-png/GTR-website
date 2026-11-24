# Deploying on Coolify

The repository is ready to deploy as a Dockerfile-based Coolify application. No server, domain, database, or live email account has been configured from this repository.

## 1. Create the application

1. In Coolify, create a resource from this Git repository and select **Dockerfile** as the build pack.
2. Set the Dockerfile path to `Dockerfile` and the build context to the repository root.
3. Configure the application to expose port `8000`. The container listens on `8000` by default; only set `PORT` if you also configure Coolify to expose that same port.
4. For SQLite, add a Coolify persistent storage volume mounted at `/data` in the container. For PostgreSQL instead, attach or create a service on the private Coolify network and use its internal hostname—not `localhost`.
5. Add your domain in Coolify and enable its HTTPS certificate/proxy.

At startup the container applies migrations, collects static assets, then starts Waitress. WhiteNoise serves `/static/` from the collected directory. For SQLite, the `/data` volume must be persistent and writable by the container's `django` user or inquiry data will be lost on redeploy.

## 2. Add environment variables

Add these as Coolify runtime environment variables/secrets. Do not commit them or put real credentials in `.env.example`.

| Variable | Value |
| --- | --- |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `SECRET_KEY` | Unique random secret, at least 50 characters |
| `ALLOWED_HOSTS` | Domain name(s), comma-separated, no scheme (for example `www.example.com,example.com`) |
| `CSRF_TRUSTED_ORIGINS` | HTTPS origin(s), comma-separated (for example `https://www.example.com,https://example.com`) |
| `DB_ENGINE` | Set to `sqlite` to use SQLite, or `postgresql` to use PostgreSQL (default) |
| `SQLITE_PATH` | SQLite database file path; defaults to `/data/db.sqlite3`. Keep it under the mounted `/data` volume |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | Restricted PostgreSQL application user |
| `DB_PASSWORD` | PostgreSQL application password |
| `DB_HOST` | Internal hostname of the Coolify PostgreSQL service |
| `DB_PORT` | `5432`, unless the database service specifies another port |
| `DB_SSLMODE` | Use `disable` only for private Coolify PostgreSQL traffic without TLS; otherwise use `verify-full` and configure the required CA support |
| `EMAIL_HOST` | SMTP server hostname |
| `EMAIL_PORT` | SMTP port (typically `587` for STARTTLS) |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `EMAIL_USE_TLS` | `true` for STARTTLS, or `false` when using implicit SSL |
| `EMAIL_USE_SSL` | `false` for STARTTLS, or `true` for implicit SSL |
| `DEFAULT_FROM_EMAIL` | Verified sender address for your domain |
| `CONTACT_RECIPIENTS` | Approved inquiry recipient address(es), comma-separated |
| `TRUST_HTTPS_PROXY` | Set to `true` for the HTTPS domain routed through Coolify's proxy; leave `false` if the app is not behind a trusted HTTPS-terminating proxy |

Generate `SECRET_KEY` locally, for example with `python -c "import secrets; print(secrets.token_urlsafe(48))"`. Keep it private. Do not use `*` for `ALLOWED_HOSTS`. Set exact hostnames and HTTPS origins, with no trailing slash on the origin.

Do not override `DJANGO_SETTINGS_MODULE` to development settings. Do not expose the container directly to the public internet outside Coolify's proxy.

### SQLite notes

For SQLite, set `DB_ENGINE=sqlite` and mount a persistent Coolify volume at `/data`. `SQLITE_PATH` is optional unless you want a different database file path. Do not add the `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, or `DB_SSLMODE` variables for this mode. SQLite is suitable for a small, single-instance site; do not run multiple app replicas against the same SQLite file. Back up the persistent volume regularly.

## 3. First deployment and verification

Deploy, then check the Coolify build/runtime logs for successful migrations and startup. Visit the HTTPS domain and confirm:

- The home page loads over HTTPS.
- CSS, images, and Django Admin assets load from `/static/`.
- `/admin/` is reachable and an administrator you created can sign in.
- A test contact request is saved and delivered to the configured mailbox.

Create an admin using Coolify's application terminal after the first deployment:

```sh
python manage.py createsuperuser
```

Do not use a public shell or commit admin credentials. Validate SMTP delivery with a controlled test before accepting real inquiries. The app deliberately refuses to start when required production settings are absent.

## Operations and data safety

- Back up the SQLite persistent volume or PostgreSQL database regularly and test restoration.
- The database holds contact inquiries; restrict admin access and follow your approved retention policy.
- Run `python manage.py cleanup_rate_limits` on a daily schedule if desired.
- The entrypoint runs migrations at each container start. For multi-replica PostgreSQL deployments, serialize migrations or use a separate controlled migration step.
- Roll back application code only when it is compatible with the database schema already migrated.

For local production-setting checks and general deployment guidance, keep the production-only environment values out of source control and use Coolify's secret management.
