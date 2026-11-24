from django.urls import path
from django.views.generic import RedirectView
from . import views
from .pages import PAGES

app_name = 'website'
urlpatterns = []
for name, (route, source) in PAGES.items():
    urlpatterns.append(path(route, views.page, {'page_key': name}, name=name))
    urlpatterns.append(path(source, RedirectView.as_view(pattern_name='website:' + name, permanent=True)))
urlpatterns.append(path('contact.html', RedirectView.as_view(pattern_name='inquiries:contact', permanent=True)))
