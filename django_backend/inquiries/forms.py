import time
import uuid
from django import forms
from django.conf import settings
from django.core import signing
from .models import Inquiry

TOKEN_SALT = 'grittech.contact.v1'


def new_submission_token():
    return signing.dumps({'id': str(uuid.uuid4()), 'started': time.time()}, salt=TOKEN_SALT)


class InquiryForm(forms.ModelForm):
    submission_token = forms.CharField(widget=forms.HiddenInput)
    website_url = forms.CharField(required=False)  # Honeypot; genuine visitors leave it empty.

    class Meta:
        model = Inquiry
        fields = ['full_name', 'email', 'phone', 'company', 'subject', 'message']

    def clean_subject(self):
        value = self.cleaned_data['subject']
        if '\r' in value or '\n' in value:
            raise forms.ValidationError('Please enter the subject on one line.')
        return value

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('website_url'):
            raise forms.ValidationError('Unable to accept this submission. Please try again.')
        try:
            data = signing.loads(cleaned.get('submission_token', ''), salt=TOKEN_SALT, max_age=3600)
            self.submission_uuid = uuid.UUID(data['id'])
            elapsed = time.time() - float(data['started'])
            if elapsed < settings.CONTACT_MIN_SECONDS:
                raise ValueError('too fast')
        except (signing.BadSignature, ValueError, KeyError, TypeError):
            raise forms.ValidationError('Please reload the form and try again after a few seconds.')
        return cleaned
