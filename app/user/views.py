"""
view for the user API

"""

from rest_framework import generics, authentication, permissions

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.settings import api_settings

from user.serializers import UserSerializer

from user.serializers import AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagerUserView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrive the authenrcated user"""
        return self.request.user
