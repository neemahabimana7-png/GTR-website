# Grittech Resources — isolated Django integration

The existing website is preserved in the parent folder. **Run Django from this folder, `django_backend`, not from the original frontend root.** No original HTML, CSS, JavaScript, images, configuration, README or Git ignore file was edited.

## Start in VS Code on Windows

Open a terminal and run:

```powershell
cd "C:\Users\USER\Desktop\EPCA websites\GTR-website\django_backend"
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

Open http://127.0.0.1:8000/. `start-local.cmd` runs the last command. Stop with Ctrl+C. No activation is necessary when using the full virtual-environment Python path. The currently prepared environment uses Python 3.12.14; virtual environments are machine-specific, so recreate it when moving the project.

## Create your own administrator

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own username, email and strong password interactively. No administrator or default password was created by this integration. Open http://127.0.0.1:8000/admin/. See [the admin guide](docs/ADMIN_GUIDE.md) before granting staff permissions.

## Contact form

Visit `/contact/`, complete required fields and wait at least two seconds before submitting. Inquiries are stored in `.local/db.sqlite3`. Development notifications print in the server terminal: they are **not sent to the internet**. `development@localhost` and `local-review@localhost` are local test placeholders, not company email addresses. Database storage remains successful even when email fails.

## Verification

```powershell
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe scripts\verify_frontend.py
```

The second command compares parent originals to the pre-integration backup hashes and compares all rendered pages with the originals. It will correctly report changes if you intentionally edit originals later. Do not rewrite the baseline to hide changes.

## What is implemented

- All 12 original pages and old `.html` redirects, including both partnership variants.
- Copied templates, exact copied CSS/images and unchanged inline JavaScript.
- Contact validation, CSRF, expiring signed form tokens, honeypot and rate limits.
- Inquiry persistence, duplicate-submit protection and company email notifications.
- Django Admin inquiry search, filtering, status/notes and notification retry.
- Fail-closed PostgreSQL/SMTP/HTTPS production settings; no production deployment.

Start with [SETUP](docs/SETUP.md), [ARCHITECTURE](docs/ARCHITECTURE.md), and the [learning index](docs/learning/README.md). Known frontend issues are recorded in [FRONTEND-PRESERVATION](docs/FRONTEND-PRESERVATION.md), not silently redesigned.
