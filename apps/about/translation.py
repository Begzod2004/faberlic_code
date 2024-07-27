from modeltranslation.translator import TranslationOptions, register

from apps.about.models import *


@register(Contact)
class ContactTranslation(TranslationOptions):
    fields = ("address",)


@register(Service)
class ServiceTranslation(TranslationOptions):
    fields = ("title", "sub_title")
