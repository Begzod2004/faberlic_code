from rest_framework.serializers import ModelSerializer

from apps.about.models import Contact, Service, Social
from apps.utils import SymbolValidationMixin


class ContactUsSerializer(SymbolValidationMixin, ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            "id",
            "address_uz",
            "address_ru",
            "phone_1",
            "phone_2",
            "email",
            "map",
        )  # noqa


class SocialSerializer(SymbolValidationMixin, ModelSerializer):
    class Meta:
        model = Social
        fields = ("id", "instagram", "facebook", "telegram")


class ServiceSerializer(SymbolValidationMixin, ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "title_uz", "title_ru", "sub_title_uz", "sub_title_ru", "image")
