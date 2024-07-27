from modeltranslation.translator import TranslationOptions, register

from apps.product.models import (Banner, Brand, Category, Characteristics,
                                 IndexCategory, Product, ShortDescription,
                                 Stock, SubCategory)


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ("title",)


@register(SubCategory)
class SubCategoryTranslation(TranslationOptions):
    fields = ("title",)


@register(Brand)
class BrandTranslation(TranslationOptions):
    fields = ("title",)


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = (
        "title",
        "description",
    )


@register(ShortDescription)
class ShortDescriptionTranslation(TranslationOptions):
    fields = ("key", "value")


@register(Characteristics)
class CharacteristicsTranslation(TranslationOptions):
    fields = ("key", "value")


@register(IndexCategory)
class IndexCategoryTranslation(TranslationOptions):
    fields = ("title",)


@register(Banner)
class BannerTranslation(TranslationOptions):
    fields = ("web_image", "rsp_image")


@register(Stock)
class StockTranslation(TranslationOptions):
    fields = ("title",)
