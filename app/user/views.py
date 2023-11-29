"""
Views for the user API
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializers, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    # This is the renderer class that will be used to render the browsable API.
    # We need to add this because we have added a custom renderer class in the
    # settings.py file.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
