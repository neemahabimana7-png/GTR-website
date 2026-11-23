# Templates and static files

A Django template is HTML plus server-side instructions. A tag such as `{% url ... %}` performs an action; `{{ ... }}` outputs a value. Filters transform values, for example `default_if_none` keeps a blank form field blank instead of showing None. Django normally escapes output, so a visitor's angle brackets become text rather than active HTML.

Your copied pages begin with this actual pattern:

```django
{% extends "base.html" %}{% load static %}{% block document %}
```

`extends` selects a parent template. A `block` fills a replaceable area in that parent. Here `base.html` has a full-document block: it is intentionally modest so each original page keeps its exact head, stylesheet order, body classes and scripts. A more aggressive base layout might accidentally remove page-specific CSS or change the design.

Exact navbar/footer markup is extracted into `templates/includes/`. Copied pages use `{% include 'includes/...' %}`. Different original variants remain different includes, so stale labels are documented rather than silently standardized. Hash-like filenames identify exact markup variants, not new business entities.

```django
{% static 'frontend/grittech.css' %}
{% url 'website:home' %}
{{ form.full_name.value|default_if_none:'' }}
```

`load static` enables the static tag in the current template. The static tag produces a URL; it does not read an image into Python. In development Django serves those assets; production collects and serves them separately. CSS files and image files are exact copies, with their original relative relationships preserved. Existing CDN references remain external.

The copied contact form keeps original inputs rather than using `form.as_p`, which would change markup. Required/name/value bindings and conditional error includes connect it to Django. Visible content outside form feedback remains equivalent to the original. The preservation script checks the resulting DOM and unchanged inline JavaScript.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

template, extends, block, include, static, autoescape.

## Review questions

1. Why keep a full-document block?
2. Does static load file bytes into a view?
3. Why not use form.as_p here?

## Safe practical exercise

Open a copied page and follow one navbar include. Find its original href converted to a named URL and its logo src converted to static.

**Expected result:** You can trace an unchanged logo and navigation item from original markup through Django rendering.
