# Forms and validation

An HTML form collects input. A Django Form checks that input on the server. The browser can enforce required fields, but a client can bypass browser checks. InquiryForm is a ModelForm: it reuses the Inquiry field definitions while adding submission_token and website_url anti-abuse fields.

```python
# Actual contact view flow
form = InquiryForm(request.POST)
if form.is_valid():
    fields = {name: form.cleaned_data[name] for name in form.Meta.fields}
```

Before is_valid(), POST values are untrusted strings. After success, cleaned_data contains validated, trimmed values. Required name, email, subject and message must be present. Phone and company are optional. Subject newlines are rejected and message length is capped. clean() also verifies the signed token, minimum age and empty honeypot.

The CSRF token is separate from the submission token. CSRF checks that a POST has the proper browser token. The signed submission token has an expiry, start time and UUID for spam resistance/idempotency. One does not replace the other.

Copied inputs keep their original IDs and CSS classes. Their added name attributes match form fields, and escaped bound values repopulate invalid submissions. `field_errors.html` displays errors next to the input; `form_feedback.html` displays general errors and success messages. On first GET, neither creates a visible alert.

A valid POST saves a record within a transaction and schedules notification after commit. A database uniqueness constraint, not just JavaScript, prevents duplicate UUIDs. The response redirects to GET. A notification failure does not invalidate the database save or ask the visitor to submit repeatedly. An invalid form returns errors without saving a record. Rate limiting applies even to invalid attempts.

Do not make internal_notes or status public fields. The view explicitly builds the saved field dictionary from the approved form fields, so a visitor cannot set staff workflow information by adding POST parameters.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

bound form, cleaned_data, validation, CSRF, idempotency.

## Review questions

1. Why are browser checks insufficient?
2. What is the honeypot for?
3. Can a visitor set internal notes?

## Safe practical exercise

Submit the local Contact form with a deliberately invalid email after disabling browser validation only in a test client, or run its invalid-email automated test.

**Expected result:** The server rejects the data, displays errors, and stores no Inquiry for that invalid attempt.
