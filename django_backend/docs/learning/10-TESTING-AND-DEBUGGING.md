# Testing and debugging

An automated test runs a controlled example and checks the result with assertions. Tests are repeatable evidence: a working-looking form does not prove that invalid messages, spam or email failure are handled safely. Django TestCase creates an isolated test database, so test messages and test admin accounts do not become real local inquiries.

`website/tests.py` checks every route, legacy redirects, unknown pages, local asset references and preservation hashes. `inquiries/tests.py` checks form fields, database saves, email headers/failures/retries, CSRF, signed-token age and expiry, honeypot, duplicate submissions, rate limits and Admin permissions.

```python
# An assertion from the actual test suite
self.assertEqual(Inquiry.objects.count(), 1)
self.assertEqual(len(mail.outbox), 1)
```

The duplicate-submission test makes the same request twice and checks these assertions: only one record and one email exist. The tests execute on_commit callbacks explicitly because Django TestCase normally wraps tests in a transaction; without that, post-commit notification work would not run in the test.

Start with the final exception line in a traceback, then read the filename/line immediately above it. A TemplateSyntaxError points to template syntax; a missing table usually means migrations were not applied; NoReverseMatch usually means a URL namespace or name is wrong. Fix the relevant layer rather than editing original CSS to hide an error.

During implementation, tests caught incorrectly escaped filter quotes in the copied Contact template. They also caught a link-test mistake that treated external CDN paths as internal routes. These were fixed in the backend/test code only. Tests then passed.

The preservation script separately checks original bytes, static copies, normalized DOMs and inline scripts. Browser screenshots, CDN availability, production SMTP and PostgreSQL connectivity are different checks; do not claim them merely because unit tests pass.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

assertion, TestCase, test database, traceback, mock.

## Review questions

1. Why use a test database?
2. Why execute on_commit callbacks in tests?
3. Does a unit test prove visual equality?

## Safe practical exercise

Run manage.py test inquiries.tests.InquiryTests.test_duplicate_submission_is_idempotent --verbosity 2.

**Expected result:** One named test passes and its temporary test database is destroyed afterward.
