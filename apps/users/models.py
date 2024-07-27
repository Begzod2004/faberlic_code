from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import BooleanField, CharField, DateTimeField, Model
from rest_framework.authtoken.models import Token

from apps.users.managers import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = None
    phone = None
    groups = None

    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    username = CharField(max_length=50, blank=True, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_staff = BooleanField(default=False)

    EMAIL_FIELD = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f"{self.username}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
