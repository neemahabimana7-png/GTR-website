# Understanding the project structure

A Django **project** is a complete configured website. A Django **app** is one coherent feature inside it. `config` is the Grittech project configuration; `website` serves public pages and `inquiries` manages customer messages. Two apps are enough here; there is no reason to create an app for every service card.

`manage.py` is the command entry point. It selects development settings by default and passes commands such as `migrate` to Django. Instead of one large settings.py, your project uses `config/settings/base.py`, `development.py` and `production.py`. Base lists middleware, templates and apps; the other two choose databases, email and environment-specific security.

`urls.py` maps addresses to views. `views.py` contains HTTP request handling. `models.py` defines Inquiry and expiring rate counters. `forms.py` validates contact input. `admin.py` controls staff access. `services.py` isolates notification sending so the view remains readable. These roles are related, but they are not interchangeable: putting SMTP logic in a template would be the wrong layer.

Templates live in `templates/`, and exact copied frontend files in `static/frontend/`. `.local/` holds local runtime state such as SQLite and the generated development secret; it is not source code and is ignored by Git. `requirements/` records Python dependencies, while the original parent's package.json still describes frontend build tooling.

```text
manage.py -> settings -> config/urls.py
                       -> website (public pages)
                       -> inquiries (form, model, notifications, Admin)
```

Python imports connect files. For example, `from .forms import InquiryForm` means the view imports a class from forms.py in the same app. An empty `__init__.py` marks a regular Python package. A migration is executable schema history; it belongs in source control, unlike the changing SQLite database.

Read the file-by-file walkthrough for actual functions and short source excerpts. You do not need to memorize every filename before following one request end to end.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

project, app, module, package, settings.

## Review questions

1. Why are there two apps?
2. Which files are runtime data?
3. What does a relative import mean?

## Safe practical exercise

Locate manage.py, inquiries/forms.py and templates/pages/contact.html in VS Code, and follow the import from inquiries/views.py to forms.py.

**Expected result:** You can identify where a contact request is received, validated and rendered without changing code.
