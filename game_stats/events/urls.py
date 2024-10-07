# events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.record_event, name='record_event'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
