"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions   #generics has the CreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import status


from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

@extend_schema(
    request=UserSerializer,
    responses={201, UserSerializer},
    # parameters=[
    #     OpenApiParameter('email', OpenApiTypes.STR, location=OpenApiParameter.QUERY, required=True),
    #     OpenApiParameter('password', OpenApiTypes.STR, location=OpenApiParameter.QUERY, required=True),
    #     OpenApiParameter('name', OpenApiTypes.STR, location=OpenApiParameter.QUERY, required=True),
    # ],
    description="Endpoint for creating a new user"
)
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer      # Uses our serializer to override the default serializer since we use email
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

