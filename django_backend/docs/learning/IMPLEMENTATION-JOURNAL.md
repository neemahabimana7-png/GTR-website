# Implementation journal — 2026-11-23

## 1. Preparation and preservation boundary

- Read the approved full brief and strict original-file instructions; reviewed the earlier 12-page static-site audit.
- Created the full ZIP before adding backend code, including original Git metadata, dependencies and untracked working files. Python ZIP CRC verification reported no corrupt member.
- Recorded hashes for 2,675 original non-Git files and documented backup location. Existing Git changes were not reset or committed.
- Created only `django_backend/` in the source repository; intermediate authoring scripts remained in the Codex task workspace.
- Problem: Windows intermittently failed to launch PowerShell/Python processes. Running the bundled Python directly through cmd.exe provided a working local path. This was an execution-environment issue, not a reason to alter the frontend.

## 2. Environment and Django configuration

- Created `.venv` with Python 3.12.14 and installed pinned Django 5.2.19 with pip. Added production driver/server requirements separately.
- Created manage.py, config/settings modules, environment loader and URL/server entry points.
- Development uses SQLite and console mail; production refuses missing private settings. No production credentials or administrator account were invented.
- Concepts: virtual environment, settings, apps, middleware, WSGI/ASGI, environment variables.

## 3. Template/static integration

- Copied all 12 HTML pages into templates/pages, preserving each original document structure/head and inline scripts.
- Added full-document base inheritance and shared exact navbar/footer variants; converted only local references to static/named-URL tags.
- Copied 36 original static assets byte-for-byte. Created template conversion and inventory JSON reports.
- Fixed the pre-existing broken Quality footer Supply Chain destination only in its copied include as a technical route binding. Preserved labels, placeholders, duplicate partnership pages and unrelated issues.
- Concepts: render, extends/block/include, staticfiles, named routes, legacy redirects.

## 4. Inquiry, security and administration

- Added models/forms/views/services/admin, signed expiring UUID submissions, honeypot, minimum age, shared database rate limits and admin-login throttling.
- Added company notification tracking and retry/expiry commands. Saving and email are separate; notifications run after successful database commit.
- Generated 0001_initial with makemigrations; applied migrations to the local SQLite database. No production database was accessed.
- Concepts: ModelForm, cleaned_data, ORM, transaction.atomic/on_commit, TextChoices, auth permissions, HTTP status codes.

## 5. Automated testing and corrections

- Initial tests found an incorrectly escaped default_if_none filter in the copied contact textarea. Corrected the copy; original contact.html never changed.
- A test initially treated CDN URL paths as local routes. Corrected the test to ignore URLs with external scheme/host, rather than changing working external frontend references.
- Reran the 33-test suite: all passed. Covered public/legacy routes, form errors/saves, CSRF, duplicate submit, token expiry/timing, honeypot, rate limits, email success/failure/retry, staff permissions and static/original hashes.
- Ran scripts/verify_frontend.py: 2,675 original files unchanged, 36 static copies equal, all 12 rendered pages structurally equivalent and all inline script bodies unchanged.

## 6. Documentation and handover

- Created README, architecture/setup/database/admin/security/deployment guides, preservation/verification records, changelog, 11 lessons, command reference and per-file walkthrough.
- Every lesson has a summary, terms, review questions and a safe exercise. Examples refer to the actual Inquiry and Grittech routes/templates.
- Deployment remains unauthorized; real SMTP credentials, PostgreSQL connectivity, domain/proxy configuration, retention and owner-created administrator remain production prerequisites.
- Final TESTING.md records additional checks and limitations; do not infer browser screenshots or live delivery from unit tests.


## 7. Final checks and disk-space recovery

- Real loopback HTTP smoke checks loaded all pages, Admin login and representative static assets. A synthetic CSRF-protected inquiry was saved, notified through console mail and removed; no production recipient was contacted.
- Production settings were checked with temporary synthetic environment values, without database/SMTP connections. Only the expected HSTS subdomain/preload warnings remained. No synthetic credentials were saved to .env or committed.
- Final static collection initially failed because Windows reported zero free disk space. Recovered space by removing only this new backend's partial static_collected output and virtual-environment __pycache__ folders, with resolved-path checks. No original assets or backup files were deleted.
- Retested check, migration drift/pending status, collectstatic, pip check, all 33 tests and frontend preservation: all passed. Removed the verified reproducible static_collected output to conserve disk space; deployers regenerate it on the target host.
- Recorded exact installed packages in requirements/locked-windows-py312.txt. Created the handover, test report and clean backend ZIP excluding .venv, .local, private .env, bytecode and collected output.
- Browser visual/responsive/animation verification remained unavailable because the browser tool could not initialize its kernel assets path. Structural/asset/script equality is verified; pixel equality and remote CDN availability are not claimed.
- The Windows volume remains low on free space. Free unrelated disk space yourself before ongoing development, package installation or deployment; the integration did not delete unrelated files.
