# profiles/urls.py
from django.urls import path
from .views import UserProfileListAPIView, get_user_profile

urlpatterns = [
    path('profiles/', UserProfileListAPIView.as_view(), name='userprofile-list'),
    path('user-profile/<int:user_id>/', get_user_profile, name='get_user_profile'),
]
