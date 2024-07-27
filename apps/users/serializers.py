from django.contrib.auth.hashers import make_password
from djoser.constants import Messages
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class RegisterModelSerializer(ModelSerializer):
    password = CharField(max_length=150)
    confirm_password = CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "confirm_password",
        )

    @staticmethod
    def check_password(**kwargs):
        if kwargs.get("password") != kwargs.get("confirm_password"):
            raise serializers.ValidationError(
                {"password_mismatch": Messages.PASSWORD_MISMATCH_ERROR}
            )
        return True

    def validate(self, attrs):
        if self.check_password(**attrs):
            attrs.pop("confirm_password")
        attrs["password"] = make_password(attrs.get("password"))
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
        ]
