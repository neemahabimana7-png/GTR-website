# Django security in this project

Security is a set of boundaries, not one setting. CSRF protects state-changing requests, validation limits accepted input, escaping keeps visitor data from becoming executable HTML, and permissions limit staff actions. Django supplies useful defaults, but configuration and operations still matter.

The form adds `{% csrf_token %}`, while CsrfViewMiddleware checks submissions. InquiryForm rejects missing/invalid fields, long messages, newline subjects, honeypot content and invalid/tampered/expired submission tokens. A valid signed token cannot replace authentication for an administrator; it only belongs to the public submission workflow.

The SECRET_KEY signs tokens and sessions. Development generates a private random secret in an ignored local file. Production requires its own long value and never falls back to that file. DEBUG=False prevents detailed error pages from exposing internals publicly. ALLOWED_HOSTS must list approved production domains.

Database-backed rate counters work across workers. The keys are hashes based on connection IP, scope and fixed time window. Raw IPs are not stored. Untrusted forwarded headers are ignored; production proxy configuration must provide genuine client addresses or many users could share one limit. Rate limits help abuse resistance but do not stop every bot or a DDoS attack.

Secure production settings require HTTPS, secure cookies, frame denial and MIME sniffing protection. Existing external scripts/inline JavaScript are preserved, so a strict new Content Security Policy was not silently added. There are no public uploads, no visitor login and no hardcoded credentials.

```python
# Actual production configuration
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

Read SECURITY.md for threat/operational limits. A deployment check is evidence about configuration, not proof that a hosting provider or database has been secured correctly.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

CSRF, escaping, secret key, permissions, rate limiting.

## Review questions

1. How does authorization differ from validation?
2. Why must DEBUG be false publicly?
3. Why ignore arbitrary forwarded IPs?

## Safe practical exercise

Run the CSRF, honeypot and admin-login rate-limit tests locally. Read the expected 403/400/429 assertions.

**Expected result:** Requests lacking the appropriate security conditions are rejected without changing the original frontend.
