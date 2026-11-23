# Models and databases

A database stores records beyond the lifetime of one request. A Django model is a Python description of one kind of record. Your Inquiry model describes a contact message, not a public user account. Django's ORM translates model operations into database queries.

```python
# Actual Inquiry fields
full_name = models.CharField(max_length=150)
email = models.EmailField()
message = models.TextField(validators=[MaxLengthValidator(5000)])
```

CharField stores a bounded string, EmailField adds email-aware validation, and TextField stores longer text. Django supplies an integer primary key, `id`, to identify each row. The separate unique submission UUID guards against duplicate POSTs. ModelForm applies field validation before saving; calling model.save() directly does not automatically perform every form validation rule.

The view uses `get_or_create(submission_id=..., defaults=...)`. If the signed submission already exists, it returns that row rather than creating another. `transaction.atomic()` treats the save as a database unit. `transaction.on_commit()` delays notification sending until the save succeeds, so a message is never emailed as accepted and then rolled back.

SQLite is a file and is convenient locally. PostgreSQL is a separate database service and is configured for production. Both use the same model/migration code, but production concurrency and connectivity still require staging tests. The auxiliary RateLimitBucket table stores only temporary security counters, not inquiries.

`makemigrations` writes a Python migration describing a schema change. `migrate` applies unapplied migrations to a database. Changing a model alone does not update an existing database. Keep migrations with the source code and back up real data before deployment.

For safe study use read-only ORM queries such as `Inquiry.objects.count()` or `Inquiry.objects.filter(status='new')`. Avoid printing real visitor messages in shared terminals. Full field definitions and backup guidance are in DATABASE.md.

## Summary

This lesson connects the concept to the running Grittech backend. Follow the actual files and use local test data before making changes.

## Terms to remember

model, ORM, primary key, migration, transaction.

## Review questions

1. Why have both id and submission_id?
2. What is the difference between makemigrations and migrate?
3. Why email only after commit?

## Safe practical exercise

In the local Django shell import Inquiry and run Inquiry.objects.count(). Do not insert, update or delete any rows.

**Expected result:** You see the number of locally stored inquiries without altering the database.
