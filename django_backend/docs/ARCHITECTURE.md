# Architecture

## Boundary

Everything added lives inside `django_backend/`. The parent static website remains the reference. The full archive path is recorded in `BACKUP-LOCATION.txt`; the original file hashes are in `frontend-original-manifest.json`.

```text
Browser GET -> config/urls.py -> website/urls.py -> website/views.py
            -> copied template -> static/frontend assets -> browser

Browser POST /contact/ -> CSRF middleware -> inquiries/views.py
 -> database rate limit -> InquiryForm validation -> atomic Inquiry save
 -> commit -> company notification -> redirect -> success message

Staff -> /admin/ -> Django authentication/permissions -> InquiryAdmin
```

## Applications

`config` is project configuration, not a business app. Its base settings list middleware, installed apps, templates, static files and common email/security options. Development provides SQLite and console email; production requires PostgreSQL, a private secret, approved hosts and email configuration.

`website` serves an explicit allowlist of templates. `PAGES` in `website/pages.py` maps each named route to its original source path. No visitor can supply an arbitrary template filename. Legacy HTML URLs redirect permanently to named routes; neither partnership variant was deleted.

`inquiries` owns business persistence and submission handling. Forms validate untrusted input. Views coordinate HTTP behavior. `services.py` sends notifications outside the save transaction. `admin.py` gives staff access without creating public visitor accounts. `security.py` and middleware provide shared database-backed rate limits.

## Templates and preservation

Each copied page extends `base.html` through a full-document block. This deliberately modest inheritance avoids normalizing page-specific heads, body classes, stylesheet order or differing footer content. Exact navbar/footer variants become shared hashed include files. The include name identifies identical markup; different footers are not silently merged.

The public form keeps its original elements and Bootstrap classes. Technical additions are field names, required/length constraints, escaped bound values, CSRF, hidden anti-abuse fields, and conditionally visible feedback. No original CSS is changed, including the CSS copies. Dynamic feedback only appears after a submission or error.

## Deliberately omitted

No CMS, public login, public API, customer database, media uploads, Redis, Celery, or service-content tables. Marketing content stays in copied templates. A future CMS needs its own approval and safe image-upload design.

## Dependencies

Django 5.2.19 is pinned in `requirements/base.txt`. PostgreSQL support and the cross-platform Waitress server are in `requirements/production.txt`. The original Node/Tailwind build remains untouched and is not required to serve the already compiled assets.
