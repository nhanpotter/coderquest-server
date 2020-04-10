from django.urls import include, path, re_path
from .views import *

urlpatterns = [
    path('send_history/', SendHistoryView.as_view(), name='send-history'),
]