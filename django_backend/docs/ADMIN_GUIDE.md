# Administrator guide

## First access

From `django_backend`, run `.\.venv\Scripts\python.exe manage.py createsuperuser`. Enter your own details and password. No account or password was pre-created. Open `/admin/` on the running local site.

Use the superuser for initial setup, then create individual staff users for daily work. `is_staff` permits attempting Admin access; it does not grant access to every model.

## Suggested staff permissions

- `view_inquiry`: read/search/filter inquiries.
- `change_inquiry`: update status and internal notes, and retry notifications.
- `delete_inquiry`: remove records only when the administrator's responsibilities require it.

Do not grant superuser status simply to make an inquiry appear. The RateLimitBucket model is not exposed for routine editing. Public inquiry creation happens through the validated contact form; adding arbitrary records in Admin is intentionally disabled.

## Processing a message

1. Search by name, email, company or subject.
2. Filter by status/date/notification status.
3. Open the inquiry and read the original details.
4. Change `New` to `In progress` while responding through your approved company communication channel.
5. Add internal notes, then mark `Closed` when complete. Mark genuine spam as `Spam`.

The website does not send a customer reply merely because you save notes. Internal notes are never included in the public form or original company-notification template.

## Notification problems

`Sent` means the configured backend accepted the notification, not proof of delivery to an inbox. In local console mode it means printed, not internet delivery. `Failed` leaves the inquiry safely stored. Select failed records and choose **Retry pending or failed company notifications** if you have change permission.

For command-line retries run `manage.py retry_notifications --limit 20`. If a process crashed while a record was `sending`, review it before using `--recover-stale`: that resets attempts older than 15 minutes. A crash after sending but before recording success can produce a duplicate notification on recovery. The original inquiry remains unique.

Admin login submissions are rate-limited to 10 per 15-minute fixed window per connection address by default. Wait after a 429 response. Production staff should use strong unique passwords and host-level MFA/SSO or restricted admin access where available; built-in password login is implemented, MFA is not.
