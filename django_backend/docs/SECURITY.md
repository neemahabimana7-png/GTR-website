# Implemented security and operational limits

## Request and form protections

- Django CSRF middleware and `{% csrf_token %}` protect contact and admin POSTs.
- ModelForm validates names, email, subject, lengths and required fields on the server. Browser validation is supplementary.
- Template autoescaping prevents submitted values becoming HTML when redisplayed.
- ORM queries avoid building SQL from strings.
- Signed one-hour submission tokens contain a UUID and start time. Two-second minimum age and a hidden honeypot discourage simple bots. UUID uniqueness prevents duplicate records for the same token.
- Contact POSTs are limited to 5 per 10-minute fixed window per connection IP; invalid attempts count too. Admin login POSTs are limited to 10 per 15 minutes. Fixed windows can allow bursts across a boundary; this is not a DDoS defense.
- Request bodies are limited to 64 KiB and field counts to 30. Add upstream body/rate limits in production too.

`REMOTE_ADDR` is the input for abuse keys. Arbitrary `X-Forwarded-For` is ignored. Behind a proxy, explicitly configure a trusted server/proxy to supply the genuine connection address; otherwise all users may share the proxy's limit. Never trust forwarding headers from arbitrary internet clients.

## Authentication and permissions

Only Django Admin has authentication; there are no public registration pages. Staff need model permissions. Original visitor information is read-only; status and notes require change permission. No default account, password, SMTP credential or database password is included.

## Email boundaries

A company-controlled sender is used; visitor email is `Reply-To`. The subject is checked for newlines. Only a notification failure and record ID are logged; the application does not log message bodies or SMTP exception details. Console mail intentionally prints the inquiry for local learning, so do not publish console logs. Retries require staff change permission or command-line access.

## Environment and production

`.env` and `.local` are ignored inside the backend. Production requires a long private secret, explicit allowed hosts, PostgreSQL credentials and approved email recipients. Production disables debug, redirects to HTTPS, uses secure cookies, enables MIME sniffing protection and a conservative one-hour HSTS policy. Only enable proxy trust when the proxy overwrites spoofed headers. Increase HSTS deliberately after verifying HTTPS; do not enable subdomain/preload policies without checking every affected host.

## What was not changed

Original assets and scripts remain exact. Pre-existing CDN/font/image dependencies, placeholder SRI values and external embeds remain as documented in FRONTEND-PRESERVATION.md. A strict Content Security Policy is not silently enabled because it would block existing inline scripts/styles and external assets. It needs a separate audited rollout. Existing frontend issues were not fixed by editing originals.

## Operations

Run tests and `check --deploy` with production settings; keep Django security patches current. Clean expired rate buckets daily, monitor failed notifications, back up the database and test restores. Select a retention policy before real public inquiries are collected. No uploaded files are accepted; adding uploads requires a new validation/storage design.
