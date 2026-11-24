from django.urls import path
from .views import contact
app_name = 'inquiries'
urlpatterns = [path('', contact, name='contact')]
