# Introduction to Django

A frontend is what the browser displays. Your original HTML creates headings and cards, CSS gives them shape and color, and JavaScript animates them. A backend runs on the server. It receives requests, checks data, uses a database and decides which response to return. Django adds those server responsibilities without replacing your existing design.

Django uses Model–View–Template (MVT). **Model** describes stored data: `Inquiry` is your visitor's message. **View** is Python that decides what to do with a request: `contact()` validates and saves a POST. **Template** is HTML with a few instructions: the copied Contact template displays the existing form and, when needed, escaped errors. The URL dispatcher chooses the view before any of this happens.

When you visit `/services/mineral-trading/`, the browser sends a GET request. `config/urls.py` includes `website.urls`. That module selects the Trading route. `website.views.page()` calls `render()` with the copied Trading template. Django sends HTML, and the browser requests styles and images from `/static/frontend/`. Your old JavaScript then runs in the browser; it does not become Python.

Submitting `/contact/` sends a POST. Unlike GET, it can create a database record. The server does not trust the form just because it looks valid in the browser. It validates it, stores it, attempts the notification and redirects to GET. That last redirect avoids sending the form again when the visitor refreshes.

```python
# Actual website/views.py
def page(request, page_key):
    return render(request, 'pages/' + PAGES[page_key][1])
```

`request` is the incoming HTTP request; `page_key` comes from your explicit route list. This view deliberately does not query a database because a marketing page does not need one.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

frontend, backend, request, response, MVT.

## Review questions

1. Which part renders the existing service cards?
2. Why is an Inquiry a model?
3. Why should a contact submission use POST?

## Safe practical exercise

Open the original homepage with Live Server, then open the Django homepage at port 8000. Compare the visible content without editing either file.

**Expected result:** The design/content should match; only the serving application and technical URL paths differ.
