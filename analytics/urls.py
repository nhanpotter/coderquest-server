from django.urls import include, path, re_path
from .views import *

urlpatterns = [
    path('send_history/', SendHistoryView.as_view(), name='send-history'),
    path('', data_analysis_home, name='data-analysis-home'),
    path('<expedition_id>/', data_analysis, name='data-analysis'),
]