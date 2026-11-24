from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import InquiryForm, new_submission_token
from .models import Inquiry
from .security import take_slot
from .services import notify_inquiry


@require_http_methods(['GET', 'HEAD', 'POST'])
def contact(request):
    status = 200
    form = InquiryForm(initial={'submission_token': new_submission_token()})
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        allowed, retry = take_slot(request, 'contact', settings.CONTACT_RATE_LIMIT, settings.CONTACT_RATE_WINDOW)
        if not allowed:
            form.is_valid()
            form.add_error(None, 'Too many submissions. Please wait a few minutes before trying again.')
            response = render(request, 'pages/contact.html', {'form': form}, status=429)
            response['Retry-After'] = str(retry)
            return response
        if form.is_valid():
            fields = {name: form.cleaned_data[name] for name in form.Meta.fields}
            with transaction.atomic():
                inquiry, created = Inquiry.objects.get_or_create(submission_id=form.submission_uuid, defaults=fields)
                if created:
                    transaction.on_commit(lambda: notify_inquiry(inquiry.pk))
            messages.success(request, 'Thank you. Your message has been received by our team.')
            return redirect('inquiries:contact')
        status = 400
    return render(request, 'pages/contact.html', {'form': form}, status=status)
