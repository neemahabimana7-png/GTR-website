# Django commands on Windows

All commands below run inside `django_backend`. Explicit interpreter paths avoid activation-policy problems. Commands that send mail or touch a database must use the intended environment.

## `python -m venv .venv`

- **What/why:** Create the isolated Python environment.
- **When:** Once on a new machine, inside django_backend.
- **Expected result:** A .venv folder appears; originals are unchanged.
- **Common problems:** Python not found: install Python or use py -3.12. Do not copy a venv from another machine.

## `.\.venv\Scripts\python.exe -m pip install -r requirements\base.txt`

- **What/why:** Install the pinned Django dependency.
- **When:** After creating the environment or updating approved requirements.
- **Expected result:** Django and its dependencies install inside .venv.
- **Common problems:** No pip: recreate with a full Python installation. Network failures need connectivity, not edits to HTML.

## `.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload`

- **What/why:** Run the local website on loopback.
- **When:** While developing and studying.
- **Expected result:** A local server starts; Ctrl+C stops it.
- **Common problems:** Port busy: use 8001. Missing tables: run migrate. Never bind a debug development server publicly.

## `.\.venv\Scripts\python.exe manage.py makemigrations inquiries`

- **What/why:** Generate schema history from model changes.
- **When:** Only after intentionally changing a model.
- **Expected result:** A new migration or No changes detected.
- **Common problems:** Wrong app name: use inquiries. Do not generate migrations for a CSS/text-only edit.

## `.\.venv\Scripts\python.exe manage.py migrate`

- **What/why:** Apply pending migrations to the selected database.
- **When:** After setup and approved schema changes.
- **Expected result:** Each migration reports OK; later runs report none pending.
- **Common problems:** Check selected settings/database before running; back up real data first.

## `.\.venv\Scripts\python.exe manage.py createsuperuser`

- **What/why:** Interactively create your private administrator.
- **When:** Initial local/admin setup, with your own chosen details.
- **Expected result:** A superuser is created after validation.
- **Common problems:** Password characters are not echoed. Missing tables: migrate first. No preset credentials exist.

## `.\.venv\Scripts\python.exe manage.py check`

- **What/why:** Run Django configuration checks.
- **When:** After configuration/code changes.
- **Expected result:** No issues or actionable error messages.
- **Common problems:** Fix the named configuration issue; do not silence it just to proceed.

## `.\.venv\Scripts\python.exe manage.py test`

- **What/why:** Run all automated tests with an isolated database.
- **When:** Before accepting backend changes.
- **Expected result:** Tests finish OK and the test DB is removed.
- **Common problems:** Read the last traceback line and the failing test name. Some tests intentionally simulate email failure.

## `.\.venv\Scripts\python.exe scripts\verify_frontend.py`

- **What/why:** Check originals, copied assets and rendered structure/scripts.
- **When:** After template integration or backend changes.
- **Expected result:** Empty original_changes/static_changes and equal DOM/JS for every page.
- **Common problems:** An intentional original edit makes the baseline mismatch; review rather than overwriting the baseline.

## `.\.venv\Scripts\python.exe manage.py collectstatic --noinput`

- **What/why:** Collect frontend and Admin assets into static_collected.
- **When:** Before an authorized production release; safe locally too.
- **Expected result:** Files copied; web server serving remains a separate step.
- **Common problems:** Missing files: check STATICFILES_DIRS and the copied tree. Do not collect into the original image/CSS directory.

## `.\.venv\Scripts\python.exe manage.py check --deploy --settings=config.settings.production`

- **What/why:** Check production configuration.
- **When:** With private, approved environment configuration.
- **Expected result:** A clean check, or specific deployment warnings/errors.
- **Common problems:** Missing secrets/DB/email cause intentional failure. This command does not deploy.

## `.\.venv\Scripts\python.exe manage.py shell`

- **What/why:** Open an interactive Django-aware Python shell.
- **When:** For local read-only exploration.
- **Expected result:** Models can be imported, e.g. from inquiries.models import Inquiry.
- **Common problems:** Exit with exit(). Avoid writing/deleting real data while learning.

## `.\.venv\Scripts\python.exe manage.py cleanup_rate_limits`

- **What/why:** Delete expired temporary abuse counters.
- **When:** Daily in production or during local maintenance.
- **Expected result:** A deleted-row count.
- **Common problems:** Does not delete inquiries. Confirm the selected settings before administrative commands.

## `.\.venv\Scripts\python.exe manage.py retry_notifications --limit 20`

- **What/why:** Retry pending/failed company notifications.
- **When:** After reviewing/configuring email delivery.
- **Expected result:** An accepted/count report.
- **Common problems:** In production this can send real email. Review recipients; --recover-stale may cause a duplicate after a crash.

## Commands used during this implementation

The local Python 3.12.14 runtime created `.venv`; pip installed requirements; makemigrations generated the initial schema; migrate initialized local SQLite; test exercised the backend; verify_frontend checked originals and rendered pages. Backup creation used Windows tar, and ZIP integrity was verified with Python. No createsuperuser or live deployment command was run on behalf of the owner. Local test accounts are temporary and removed with the test database.
