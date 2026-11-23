# URLs and views

A URL pattern is an address rule. A view is Python called after a rule matches. In this project, `config/urls.py` delegates public pages to `website.urls` and `/contact/` to `inquiries.urls`. `website/pages.py` is the explicit list of public service pages. It keeps unfamiliar original filenames separate from readable public routes.

```python
# Actual route registration in website/urls.py
urlpatterns.append(path(route, views.page, {'page_key': name}, name=name))
```

For the Trading entry, route is `services/mineral-trading/`, name is `trading`, and page_key tells the view which copied template to render. `reverse('website:trading')` builds that URL from its name. The namespace avoids collisions with another app's names. `{% url 'website:trading' %}` does the same work in HTML. Named URLs let routing change without hunting down every hardcoded link.

GET asks for a representation; POST submits data that may change stored state. The same `contact()` function handles both. On GET it creates a blank form and signed token; on POST it binds request.POST, checks limits and validates. A successful POST redirects to the named Contact route. Invalid POST data returns status 400 with the bound form and errors. Too many requests returns 429 with Retry-After.

These public views are function-based: a Python function is easy to follow for a small site. Django also offers class-based views, which group behavior into methods and can reduce repetition. The legacy redirects use Django's class-based `RedirectView`; there is no requirement to convert every page view into a class.

Unknown service paths return 404. The view does not accept arbitrary filesystem paths from the browser. This is both simpler and safer than trying to render any filename supplied in a URL.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

URL pattern, view, namespace, GET, POST, redirect.

## Review questions

1. Where is the Trading route named?
2. Why redirect after a successful POST?
3. What does status 404 mean?

## Safe practical exercise

Run manage.py shell and evaluate reverse("website:trading") after importing reverse from django.urls. Exit without writing data.

**Expected result:** The output is /services/mineral-trading/.
