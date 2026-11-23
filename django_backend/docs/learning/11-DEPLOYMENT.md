# Deployment and maintenance

Development runs on your computer with debugging, SQLite and console email. Production is a publicly reachable service with a real domain, HTTPS, PostgreSQL, an approved email provider, monitoring and backups. The project prepares production configuration but was not deployed: public deployment needs separate authorization.

`runserver` is a development server, not a public production service. The provided production requirements include Waitress, a WSGI server that also runs on Windows, and Psycopg, the PostgreSQL driver. `config/wsgi.py` selects production settings unless an explicit environment setting overrides it.

Static files are handled separately. `collectstatic` gathers the copied frontend and Django Admin assets into static_collected. A web server/platform must serve that folder under `/static/`. Collecting files alone does not make a production server serve them.

```powershell
.\.venv\Scripts\python.exe manage.py check --deploy --settings=config.settings.production
.\.venv\Scripts\python.exe manage.py collectstatic --noinput --settings=config.settings.production
```

These commands require real production configuration in the environment. A deployment check failing because DB_HOST or SECRET_KEY is missing is a useful fail-closed result, not a reason to insert fake live credentials. Do not run migrations against production while learning.

HTTPS may terminate at a reverse proxy. Configure trust only for that proxy, and ensure client IP information is replaced safely. The app's rate limits use the genuine connection address, so proxy setup affects fairness. Database SSL, backups and firewalling are also infrastructure concerns, not frontend features.

Keep dependencies updated, clean expired rate buckets, monitor failed notifications, and test database restoration. Decide retention before collecting real customer inquiries. Study the operational DEPLOYMENT.md for the actual release sequence and rollback considerations; this lesson explains why those steps exist.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

WSGI, PostgreSQL, static collection, HTTPS, backup.

## Review questions

1. Why not runserver in production?
2. What does collectstatic not do?
3. Why test a backup restore?

## Safe practical exercise

Read production.py and list the required environment variables without filling them or connecting to any external server.

**Expected result:** You can explain why local settings run safely while production refuses to start with missing secrets.
