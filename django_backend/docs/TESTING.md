# Testing and verification — 2026-11-23

## Passed

- Django system checks: no issues.
- Initial local migrations applied; migration drift check reports no changes and no pending migration.
- All 33 automated tests passed on SQLite. Temporary test accounts and inquiries were removed with the test database.
- All 12 public pages rendered successfully; every legacy HTML URL redirects to its named route.
- Internal active template references resolve; representative CSS/images and Admin login also returned HTTP 200 through the real loopback server.
- Contact valid/invalid input, optional fields, header injection, field lengths, CSRF, escaping, honeypot, minimum time, token tampering/expiry, duplicate POST, rate limits and email failure/retry behavior passed.
- Admin anonymous/nonstaff rejection, staff permission boundaries, read-only visitor data and login throttling passed.
- Original preservation: all 2,675 baseline non-Git files unchanged, including all 12 original HTML files and all 15 original CSS files.
- Copied assets: 36 byte-identical files (CSS/images). All 12 rendered pages matched normalized original DOM/content and exact inline JavaScript bodies. Only URL/static/form transport bindings were normalized.
- Real HTTP Contact submission: synthetic inquiry saved in local SQLite, success feedback returned, console backend accepted notification. Synthetic inquiry and its local test counter removed afterward.
- collectstatic completed, including Django Admin assets; pip dependency checks passed.
- Windows disk space reached zero during the first collection. Only this backend's generated caches/partial collection were removed; collection was then retested. Collected output was removed after verification to conserve space; regenerate it on the deployment host. Original/static source assets and full backup were not deleted.
- Production settings checked with temporary synthetic environment values, without contacting a database or SMTP server: no errors; warnings security.W005 and security.W021 remain intentionally because HSTS subdomains/preload need owner/domain decisions. These were not silenced.

## Not performed / remaining

- Pixel/screenshot comparison, viewport emulation, animation playback and live menu-click testing: browser tool could not initialize its kernel assets directory. DOM/asset/script preservation is strong structural evidence, not a claim of completed browser visual testing.
- Availability/appearance of remote fonts, photographs, Bootstrap/AOS/icon CDNs and Google Maps was not validated in a browser. Original references were preserved.
- Live SMTP delivery, real inbox receipt and actual PostgreSQL connectivity/concurrency require approved production infrastructure and credentials.
- No live hosting/domain changes or public production deployment occurred.
- No permanent administrator account was created. Owner must run createsuperuser.

## Evidence and repeat commands

See final-check-results.json, frontend-verification.json and http-smoke-results.json. Run commands from the backend README. The local dependency snapshot is requirements/locked-windows-py312.txt; recreate environments rather than copying .venv, especially to another operating system.
