from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import \
    TokenObtainPairView as BaseTokenObtainPairView
from rest_framework_simplejwt.views import \
    TokenRefreshView as BaseTokenRefreshView
from rest_framework_simplejwt.views import \
    TokenVerifyView as BaseTokenVerifyView

from apps.users.models import User
from apps.users.serializers import RegisterModelSerializer, UserSerializer


# User Authentication API
class TokenObtainPairView(BaseTokenObtainPairView):
    @extend_schema(tags=["user"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(BaseTokenRefreshView):
    @extend_schema(tags=["user"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(BaseTokenVerifyView):
    @extend_schema(tags=["user"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MeListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = User.objects.filter(
                username=user.username
            )  # Change 'phone' to 'username'
            return queryset
        else:
            return User.objects.none()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            return UserSerializer
        else:
            return self.serializer_class

    @extend_schema(tags=["user"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserCreateAPIView(CreateAPIView):
    serializer_class = RegisterModelSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)
    renderer_classes = [JSONRenderer]

    @extend_schema(tags=["user"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    renderer_classes = [JSONRenderer]

    @extend_schema(tags=["user"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
