# Local setup on Windows

## Existing prepared environment

Use the commands in [README](../README.md). In VS Code choose **Python: Select Interpreter** and select `.venv\Scripts\python.exe` inside `django_backend`. Do not use Live Server to submit inquiries: Live Server only serves the original static files.

## Recreate on another computer

Install a supported Python release with pip (Python 3.12 or 3.13 is appropriate for this Django branch). In a terminal inside `django_backend`:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements\base.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000 --noreload
```

On systems where `python` is not found but the Python launcher is installed, use `py -3.12 -m venv .venv`. The prepared environment used the Codex-bundled Python; this is a local convenience, not a requirement for future users. Do not copy `.venv` between machines.

## Configuration

Optionally copy `.env.example` to `.env` within this folder. The simple reader supports `NAME=value` and quoted literal values, not shell commands, interpolation, multiline values, or trailing inline comments. Existing shell variables override `.env`. No production values are provided.

Development creates a random secret once in `.local/development-secret`. This avoids a shared, hardcoded secret. Keep `.local`, `.env`, and `.venv` untracked. The backend has its own `.gitignore`; the original root `.gitignore` is unchanged.

`manage.py` defaults to `config.settings.development`. Choose production explicitly using `--settings=config.settings.production` or the shell environment. WSGI/ASGI default to production. Selecting the settings module inside `.env` is too late; do not do that.

## Static frontend

Original styles were copied without edits to `static/frontend/`. Django finds them under `/static/frontend/` in development. Do not run the original CSS build as part of this backend integration. If you intentionally develop new Tailwind utilities later, use a separate build configuration targeting copied templates and preserve the approved original CSS baseline.

## Database and mail

SQLite lives at `.local/db.sqlite3`. Use fictional test data while learning. Development mail uses the console backend and can contain inquiry personal information; do not publish terminal logs. Production configuration is explained separately in [DEPLOYMENT](DEPLOYMENT.md).

## Troubleshooting

- `No module named django`: use the `.venv` interpreter and install `requirements/base.txt`.
- PowerShell activation denied: no activation is needed; invoke `.venv\Scripts\python.exe` directly.
- Port 8000 occupied: use `runserver 127.0.0.1:8001 --noreload`.
- `no such table`: run `manage.py migrate` from the backend.
- Token message on submit: reload the contact form, wait two seconds, then submit within one hour.
- HTTP 429: wait for the limit window; do not remove production safeguards to make testing easier.
