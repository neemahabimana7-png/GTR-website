# Grittech Django backend — handover

## Implemented location

`C:\Users\USER\Desktop\EPCA websites\GTR-website\django_backend`

Only this new folder was added to the website repository. **No original HTML, CSS, JavaScript, images, package configuration, README or root ignore file was edited.** The full pre-integration backup includes Git and untracked/working changes. All 2,675 non-Git originals were verified unchanged by SHA-256.

## Backend features

- Django 5.2.19; local Python 3.12.14 virtual environment.
- config, website and inquiries packages; separate development/production settings.
- All 12 copied pages, named routes and legacy HTML redirects; both partnership variants retained.
- Copied static assets, modest base inheritance and exact navbar/footer includes without redesign.
- Contact fields, server validation, escaped bound input, feedback, CSRF, signed timed submissions, honeypot and shared database rate limits.
- SQLite local database with Inquiry plus expiring RateLimitBucket; initial migration applied.
- Inquiry Admin search/filter/status/notes, permission boundaries and notification retry.
- Console development email; safe notification-failure recording; approved SMTP settings prepared for production.
- Production PostgreSQL/HTTPS configuration, pinned dependencies, cleanup/retry commands and deployment guidance. No public accounts, uploads, CMS or production deployment.

## Local start in VS Code (PowerShell)

```powershell
cd "C:\Users\USER\Desktop\EPCA websites\GTR-website\django_backend"
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

Open http://127.0.0.1:8000/. Stop any existing server with Ctrl+C before starting another on port 8000. Use a second terminal for other commands. For a new machine see docs/SETUP.md; virtual environments are not portable.

## Administrator access

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own credentials interactively, then open http://127.0.0.1:8000/admin/. No default account/password was created. Give daily staff only view/change/delete permissions required by their role.

## Email

Development prints notifications in the server terminal and does not send external mail. The localhost sender/recipient are explicitly local test sinks, not invented company addresses. Production needs an approved sender, recipient, SMTP host/port/TLS and private credentials in environment variables; see .env.example and docs/DEPLOYMENT.md. Never put credentials in templates or original files.

## Files and study material

New source/configuration: manage.py, config/, website/, inquiries/, templates/, static/frontend/, requirements/, scripts/, README.md, CHANGELOG.md and docs/. Generated local state (.local/), collected assets and .venv/ are ignored. docs/FILES-CREATED.json lists distributable files. Existing original files modified: **none**.

Professional guides: ARCHITECTURE, SETUP, DATABASE, ADMIN_GUIDE, SECURITY, DEPLOYMENT, FRONTEND-PRESERVATION and TESTING.

Study docs/learning/01 through 11 in order. Each lesson explains Grittech examples, defines terms, asks review questions and includes a safe exercise. Use DJANGO-COMMANDS.md for Windows commands, CODE-WALKTHROUGH.md for each important Python file, and IMPLEMENTATION-JOURNAL.md for the development sequence.

## Test results

All 33 automated tests passed. Every page rendered; local assets/legacy routes resolved; real local CSRF-protected inquiry storage and console mail passed. All original file hashes, copied asset hashes, 12 page DOM comparisons and inline JavaScript comparisons passed. Migrations, collectstatic, dependency checks and system checks passed. See docs/TESTING.md and JSON evidence for details.

Browser visual/responsive/animation checks could not run because the browser tool failed to initialize. Exact design is structurally preserved, but pixel equality is not claimed. External CDN availability, real PostgreSQL and SMTP delivery remain unverified. Production checks using synthetic configuration had only the expected HSTS subdomain/preload warnings.

## Before production

Confirm hosting/domain, PostgreSQL connectivity/certificates, approved SMTP sender/recipient, administrator identities, inquiry retention, proxy/client-IP settings and backups. Run PostgreSQL/staging tests and browser visual checks, review existing frontend issues documented without changing originals, configure static serving and monitored cleanup/retry, then authorize deployment separately.

The Windows drive was full during testing and remains low on free space. Only generated backend caches/collected output were removed; originals and backup were retained. Free disk space before further installations or substantial database use.
