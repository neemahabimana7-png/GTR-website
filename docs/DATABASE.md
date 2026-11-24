# Database design and lifecycle

## Inquiry: the business record

`inquiries/models.py` defines `Inquiry`. Django creates a numeric primary key `id`. A separate unique `submission_id` UUID prevents the same signed browser submission from creating two records.

| Fields | Types and purpose |
|---|---|
| full_name | CharField(150), required |
| email | EmailField, required reply address |
| phone | CharField(50), optional; preserves international formatting |
| company | CharField(200), optional |
| subject | CharField(200), required, single-line form validation |
| message | TextField, maximum 5,000 characters through validation |
| status | new / in_progress / closed / spam; indexed |
| internal_notes | Staff-only TextField |
| created_at / updated_at | Timezone-aware creation/update timestamps |
| notification_status | pending / sending / sent / failed |
| notification_attempts | Positive integer attempt count |
| notification_sent_at / notification_attempted_at | Nullable notification timestamps |

The original visitor fields are read-only in Admin. Status and internal notes are editable with change permission. Records are ordered newest first. No public endpoint lists inquiries.

## RateLimitBucket: short-lived security data

This small auxiliary table stores `key` (hashed primary key), `attempts`, and `expires_at`. The hash includes an HMAC of the scope, connection address and time window. It does not store a raw IP address. It is not a customer or analytics table. Counters use database updates, so production workers share the same limit rather than each having their own in-memory limit.

Run `manage.py cleanup_rate_limits` daily to delete expired rows. Expired counters do not continue blocking requests because new windows use new keys. At high traffic, retention cleanup and edge rate limits are important.

## Relationships

There are no custom foreign keys: an inquiry does not require a visitor account. Django also creates auth user/group/permission tables, sessions, content types, migration history and admin log tables. The admin log records staff actions through Django's built-in facilities.

## Migrations

`inquiries/migrations/0001_initial.py` creates both custom tables. `makemigrations` compares model definitions to migration history and writes schema instructions. `migrate` applies those instructions to the selected database. Commit migrations; do not delete or rewrite an applied production migration to hide a change.

Development SQLite is `.local/db.sqlite3`. Production uses a separate PostgreSQL database configured through environment variables. Running the SQLite tests does not prove PostgreSQL connectivity. Never copy development data to production without an explicit data-migration decision.

## Backup and retention

Stop local writes before copying the SQLite file, or use SQLite's online backup facility. For PostgreSQL use provider backups or `pg_dump` and test restoration to a separate database. Keep backups private and encrypted. No retention period was invented: the company must choose how long to retain inquiries. Deletion needs the corresponding Admin permission.
