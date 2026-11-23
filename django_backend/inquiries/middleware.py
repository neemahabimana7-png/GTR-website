from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from .security import take_slot


class AdminLoginThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == reverse('admin:login'):
            allowed, retry = take_slot(request, 'admin-login', settings.ADMIN_LOGIN_RATE_LIMIT, settings.ADMIN_LOGIN_RATE_WINDOW)
            if not allowed:
                response = HttpResponse('Too many login attempts. Please try again later.', status=429)
                response['Retry-After'] = str(retry)
                return response
        return self.get_response(request)
