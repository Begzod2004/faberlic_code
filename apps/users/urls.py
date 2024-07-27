from django.urls import path

from apps.users.views import (MeListAPIView, TokenObtainPairView,
                              TokenRefreshView, TokenVerifyView,
                              UserCreateAPIView, UserListAPIView)

urlpatterns = [
    path("user/register", UserCreateAPIView.as_view(), name="register"),
    path("user/list", UserListAPIView.as_view(), name="list"),
    path("user/me", MeListAPIView.as_view(), name="me"),
    path(
        "user/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # Default SimpleJWT view
    path(
        "user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Default SimpleJWT view
    path(
        "user/token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),  # Default SimpleJWT view
]
