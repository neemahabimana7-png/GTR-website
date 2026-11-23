# Email integration

SMTP is a protocol for handing a message to an email server. Django hides much of that plumbing behind an email backend. In development this project uses ConsoleEmailBackend: the message prints in the terminal and no network email is sent. The test suite uses locmem, which stores messages in mail.outbox for assertions.

```python
# Actual notification construction, simplified to its central fields
email = EmailMessage(
    subject=f'Website inquiry #{inquiry.pk}: {inquiry.subject}',
    body=render_to_string('emails/inquiry.txt', {'inquiry': inquiry}),
    from_email=settings.DEFAULT_FROM_EMAIL,
    to=settings.CONTACT_RECIPIENTS, reply_to=[inquiry.email],
)
```

The company-controlled sender is From. The visitor belongs in Reply-To. Using a visitor address as From can cause spoofing/deliverability problems. Production SMTP host, port, TLS/SSL, credentials, sender and recipients come from private configuration; they are not invented from a website address.

The service claims pending/failed records by changing status to sending, increments attempts, and then sends. If the backend accepts one message, status becomes sent with a timestamp. Exceptions or an empty recipient list mark failed; the original Inquiry remains. No sensitive exception string or full message is written to application failure logs.

An accepted backend message is not proof of final inbox delivery. In local console mode sent means printed. Staff can retry failed notifications through Admin; command-line retry supports reviewed crash recovery. A process crash between sending and recording success may lead to a duplicate email after recovery. That is distinct from duplicate inquiry storage, which is protected by UUID uniqueness.

The console can show personal information, so only use it for development. Production setup and actual mailbox verification remain operator tasks; no external email was sent during automated tests.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

SMTP, backend, From, Reply-To, notification status.

## Review questions

1. Does console mode send real email?
2. Why not use the visitor as From?
3. What happens when SMTP fails?

## Safe practical exercise

Run test_email_failure_never_loses_inquiry and test_failed_notification_can_be_retried from inquiries.tests.InquiryTests.

**Expected result:** Both tests pass: failed delivery preserves data and a later retry can succeed without a second inquiry.
