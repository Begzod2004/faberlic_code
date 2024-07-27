from django.core.validators import EmailValidator, RegexValidator, URLValidator
from django.db.models import (CharField, DateTimeField, EmailField, ImageField,
                              IntegerField, Model, URLField)

from apps.utils import generate_unique_filename


class Contact(Model):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_1 = CharField(
        validators=[phone_regex], max_length=17, blank=True, unique=True
    )
    phone_2 = CharField(
        validators=[phone_regex], max_length=17, blank=True, unique=True
    )
    address = CharField(max_length=255)
    email = EmailField(max_length=255, unique=True, validators=[EmailValidator])
    map = CharField(max_length=400)


class Social(Model):
    instagram = URLField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        validators=[
            URLValidator,
        ],
    )
    facebook = URLField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        validators=[
            URLValidator,
        ],
    )
    telegram = CharField(max_length=255, blank=True, null=True, unique=True)


class Service(Model):
    title = CharField(max_length=255, null=True, blank=True)
    sub_title = CharField(max_length=255, null=True, blank=True)
    image = ImageField(upload_to=generate_unique_filename, null=True, blank=True)
