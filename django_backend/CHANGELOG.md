# Changelog

## 2026-11-23 — isolated Django backend

- Added `django_backend/` with config, website and inquiries applications.
- Copied 12 original pages into templates; introduced technical static/named-URL bindings and exact navbar/footer includes.
- Copied original frontend assets without changing CSS or JavaScript.
- Added Inquiry persistence, idempotent contact submissions, validation, CSRF, honeypot, signed timing tokens and database-backed rate limits.
- Added staff inquiry administration, safe notification failure tracking and retry/cleanup commands.
- Added local SQLite/console email and fail-closed PostgreSQL/SMTP/HTTPS production configuration.
- Added automated integration/security tests, frontend hash/DOM verification, professional guides and 11 project-based learning lessons.
- Kept every original non-Git file unchanged; no production deployment or credentials were created.
