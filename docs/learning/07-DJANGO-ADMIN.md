# Django Admin

Django Admin is a staff interface for registered models. It is not a customer portal. `@admin.register(Inquiry)` connects the model to InquiryAdmin. The configuration controls list columns, search, filters, read-only fields and actions without building a separate dashboard.

```python
# Actual InquiryAdmin options
list_display = ['id', 'full_name', 'subject', 'status', 'created_at', 'notification_status']
list_filter = ['status', 'notification_status', 'created_at']
search_fields = ['full_name', 'email', 'company', 'subject']
```

`createsuperuser` creates an account with broad privileges; choose the details yourself. No account or password is supplied in the code. An ordinary user with is_staff can attempt Admin access but still needs permissions on Inquiry. Authentication means proving identity; authorization means being permitted to view, change or delete a record.

Original visitor fields are read-only so staff do not accidentally rewrite what the visitor sent. Status and internal_notes support follow-up. `has_add_permission()` returns False: staff do not bypass the public validation flow by adding inquiries directly. Delete permission is separate and should follow the company's retention policy.

The retry_notifications action requires change permission. It calls the same notification service as the contact view, so retry behavior is not duplicated. Admin shows the original message using escaped rendering; a visitor's HTML is not executed.

The login middleware limits POST attempts by connection address, but is not multifactor authentication. Use strong individual passwords and production admin restrictions. Read ADMIN_GUIDE.md for daily workflow and recovery commands. Exercises should use local test staff, never shared default production credentials.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

staff, superuser, authentication, authorization, ModelAdmin.

## Review questions

1. Does is_staff grant every permission?
2. Why are visitor fields read-only?
3. Which permission allows notification retry?

## Safe practical exercise

Create your own local superuser interactively, log in, and inspect the Inquiry list and filters. Do not grant anyone production access.

**Expected result:** You can reach the staff interface and understand why an ordinary unprivileged staff account would not see inquiries.
