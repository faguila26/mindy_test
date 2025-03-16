# profiles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user-profile/<int:user_id>/', views.get_user_profile, name='get_user_profile'),
]
