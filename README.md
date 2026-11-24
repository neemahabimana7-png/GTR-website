# Grittech Resources website

Django website with a PostgreSQL-backed contact form and Django Admin.

## Local development

Install Python 3.12, then from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements\base.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

The development settings use local SQLite and console email. Create a local admin with `.\.venv\Scripts\python.exe manage.py createsuperuser`.

## Coolify deployment

Deploy this repository using its root [Dockerfile](Dockerfile) and expose container port `8000`. The container uses production settings, applies migrations, collects static files, and serves the application with Waitress and WhiteNoise. Configure PostgreSQL, HTTPS domain, SMTP, and required secrets in Coolify.

See the [Coolify deployment guide](docs/DEPLOYMENT.md) for the full setup and environment-variable list. Never commit production secrets or use development settings on a public deployment.
