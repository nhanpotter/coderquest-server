from django.urls import include, path, re_path
from .views import *

urlpatterns = [
    path('activate/<uid>/<token>/', account_activate, name='account-activation'),
    path('avatar/', AvatarView.as_view(), name='avatar'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]