from django.urls import path
from django_api.views import *

urlpatterns = [
    path('settings/<str:username>',view_settings, name='settings'),
]