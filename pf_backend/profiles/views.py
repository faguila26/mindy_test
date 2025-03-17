from django.shortcuts import render
from .models import UserProfile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
# profiles/views.py
from .serializers import UserProfileSerializer

# profiles/views.py

@api_view(['GET'])
def get_user_profile(request, user_id):
    try:
        profile = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        raise NotFound(detail="UserProfile not found")

    return Response({
        'id': profile.id,
        'email': profile.email,
        'next_available_slot': profile.next_available_slot,
    })

class UserProfileListAPIView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer