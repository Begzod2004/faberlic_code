from typing import Any, Dict, List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Max, Min
from rest_framework import serializers
from rest_framework.fields import ImageField, ListField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.product.models import (Banner, Brand, Category,
                                 Images, IndexCategory, Order, OrderUser,
                                 Product, ShortDescription, Stock, SubCategory)
from apps.utils import SymbolValidationMixin
from config import settings


class ImageModelSerializer(ModelSerializer):
    uploaded_images = ListField(child=ImageField(max_length=1000000), write_only=True)

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context["request"].method

        if request_method == "POST":
            fields.pop("image", None)
        return fields

    class Meta:
        model = Images
        fields = ("id", "image", "uploaded_images")

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        created_images = []

        for image_data in uploaded_images:
            created_image = Images.objects.create(image=image_data)
            created_images.append(created_image)

        return created_images


class SubBrandSerializer(ModelSerializer):
    min_price = SerializerMethodField()
    max_price = SerializerMethodField()

    @staticmethod
    def get_min_price(obj) -> float:
        return obj.products.aggregate(Min("price"))["price__min"] or 0.0

    @staticmethod
    def get_max_price(obj) -> float:
        return obj.products.aggregate(Max("price"))["price__max"] or 0.0

    class Meta:
        model = Brand
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "min_price",
            "max_price",
        )


class SubCategorySerializer(ModelSerializer):
    min_price = SerializerMethodField()
    max_price = SerializerMethodField()
    categories = SerializerMethodField()
    brands = SerializerMethodField()

    def get_fields(self):
        fields = super().get_fields()
        request_method = (
                self.context.get("request", None) and self.context["request"].method
        )

        if request_method and request_method in ["GET"]:
            fields.pop("category", None)

        return fields

    @staticmethod
    def get_min_price(obj) -> float:
        return obj.products.aggregate(Min("price"))["price__min"] or 0.0

    @staticmethod
    def get_max_price(obj) -> float:
        return obj.products.aggregate(Max("price"))["price__max"] or 0.0

    @staticmethod
    def get_brands(obj: SubCategory) -> list:
        brands = obj.brands.all()
        return SubBrandSerializer(brands, many=True).data

    @staticmethod
    def get_categories(obj: SubCategory) -> Optional[Dict[str, str]]:
        category = getattr(obj, "category", None)
        if category:
            return {
                "id": category.id,
                "title_uz": category.title_uz,
                "title_ru": category.title_ru,
            }
        else:
            raise ValueError("Sub-category is not available.")

    class Meta:
        model = SubCategory
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "category",
            "categories",
            "min_price",
            "max_price",
            "brands",
        )


class CategoryCountSerializer(ModelSerializer):
    count = SerializerMethodField()

    @staticmethod
    def get_count(obj) -> int:
        return Category.objects.filter(is_index=True).count()

    class Meta:
        model = Category
        fields = ("count",)


class BrandAllSerializer(ModelSerializer):
    min_price = SerializerMethodField()
    max_price = SerializerMethodField()

    @staticmethod
    def get_min_price(obj) -> float:
        return obj.products.aggregate(Min("price"))["price__min"] or 0.0

    @staticmethod
    def get_max_price(obj) -> float:
        return obj.products.aggregate(Max("price"))["price__max"] or 0.0

    class Meta:
        model = Brand
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "min_price",
            "max_price",
        )


class SubCategoryAllSerializer(ModelSerializer):
    min_price = SerializerMethodField()
    max_price = SerializerMethodField()
    brands = BrandAllSerializer(many=True, read_only=True)

    @staticmethod
    def get_min_price(obj) -> float:
        return obj.products.aggregate(Min("price"))["price__min"] or 0.0

    @staticmethod
    def get_max_price(obj) -> float:
        return obj.products.aggregate(Max("price"))["price__max"] or 0.0

    class Meta:
        model = SubCategory
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "min_price",
            "max_price",
            "brands",
        )


class BrandSerializer(ModelSerializer):
    min_price = SerializerMethodField()
    max_price = SerializerMethodField()
    sub_categories = SerializerMethodField()
    categories = SerializerMethodField()

    @staticmethod
    def get_min_price(obj) -> float:
        return obj.products.aggregate(Min("price"))["price__min"] or 0.0

    @staticmethod
    def get_max_price(obj) -> float:
        return obj.products.aggregate(Max("price"))["price__max"] or 0.0

    @staticmethod
    def get_sub_categories(obj) -> list:
        brand_sub_categories = SubCategory.objects.filter(brands=obj).distinct()

        sub_category_info = [
            {
                "id": sub_category.id,
                "title_uz": sub_category.title_uz,
                "title_ru": sub_category.title_ru,
            }
            for sub_category in brand_sub_categories
        ]

        return sub_category_info if sub_category_info else None

    @staticmethod
    def get_categories(obj) -> list:
        brand_sub_categories = SubCategory.objects.filter(brands=obj).distinct()
        categories = Category.objects.filter(
            sub_categories__in=brand_sub_categories
        ).distinct()

        category_info = [
            {
                "id": category.id,
                "title_uz": category.title_uz,
                "title_ru": category.title_ru,
            }
            for category in categories
        ]

        return category_info if category_info else None

    def get_fields(self):
        fields = super().get_fields()
        request_method = (
            self.context["request"].method if "request" in self.context else None
        )
        if request_method and request_method in ["GET"]:
            fields.pop("sub_category", None)
        return fields

    class Meta:
        model = Brand
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "min_price",
            "max_price",
            "sub_category",
            "sub_categories",
            "categories",
        )


class AllCategorySerializer(ModelSerializer):
    sub_categories = SubCategoryAllSerializer(many=True, read_only=True)

    min_price = SerializerMethodField()
    max_price = SerializerMethodField()
    brands = SerializerMethodField()

    # sub_categories = SerializerMethodField()

    @staticmethod
    def get_brands(obj) -> list:
        sub_categories = obj.sub_categories.all()
        processed_brand_ids = set()  # To keep track of processed brand ids
        brand_info = []

        for sub_category in sub_categories:
            brands = sub_category.brands.all().distinct()

            for brand in brands:
                if brand.id not in processed_brand_ids:  # Check if brand already processed
                    brand_categories = Category.objects.filter(
                        sub_categories=sub_category
                    ).distinct()

                    min_price = brand.price_range.get("min", 0.0)
                    max_price = brand.price_range.get("max", 0.0)

                    brand_data = {
                        "id": brand.id,
                        "title_uz": brand.title_uz,
                        "title_ru": brand.title_ru,
                        "min_price": min_price,
                        "max_price": max_price,
                        "sub_categories": SubCategoryAllSerializer(sub_category).data,
                        "categories": [
                            {
                                "id": category.id,
                                "title_uz": category.title_uz,
                                "title_ru": category.title_ru,
                            }
                            for category in brand_categories
                        ],
                    }

                    brand_info.append(brand_data)
                    processed_brand_ids.add(brand.id)  # Add brand id to processed set

        return brand_info if brand_info else None

    @staticmethod
    def get_sub_categories(obj) -> list:
        sub_categories_info = []

        for sub_category in obj.sub_categories.all():
            # Use the SubCategoryAllSerializer to serialize sub_category
            sub_category_data = SubCategoryAllSerializer(sub_category).data
            sub_categories_info.append(sub_category_data)

        return sub_categories_info if sub_categories_info else None

    @staticmethod
    def get_min_price(obj) -> float:
        return (
                obj.sub_categories.aggregate(Min("products__price"))["products__price__min"]
                or 0.0
        )

    @staticmethod
    def get_max_price(obj) -> float:
        return (
                obj.sub_categories.aggregate(Max("products__price"))["products__price__max"]
                or 0.0
        )

    class Meta:
        model = Category
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "image",
            "is_index",
            "min_price",
            "max_price",
            "brands",
            "sub_categories",
        )


class CategorySerializer(ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    min_price = SerializerMethodField()
    max_price = SerializerMethodField()
    count = SerializerMethodField()
    brands = SerializerMethodField()

    @staticmethod
    def get_brands(obj) -> list:
        sub_categories = obj.sub_categories.all()
        category_brands = Brand.objects.filter(
            sub_category__in=sub_categories
        ).distinct()
        brand_info = [
            {"id": brand.id, "title_uz": brand.title_uz, "title_ru": brand.title_ru}
            for brand in category_brands
        ]
        return brand_info if brand_info else None

    @staticmethod
    def get_count(obj) -> int:
        return Category.objects.filter(is_index=True).count()

    @staticmethod
    def get_min_price(obj) -> float:
        return (
                obj.sub_categories.aggregate(Min("products__price"))["products__price__min"]
                or 0.0
        )

    @staticmethod
    def get_max_price(obj) -> float:
        return (
                obj.sub_categories.aggregate(Max("products__price"))["products__price__max"]
                or 0.0
        )

    class Meta:
        model = Category
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "image",
            "is_index",
            "count",
            "min_price",
            "max_price",
            "brands",
            "sub_categories",
        )


class ShortDescriptionSerializer(ModelSerializer):
    class Meta:
        model = ShortDescription
        fields = (
            "id",
            "key_uz",
            "key_ru",
            "value_uz",
            "value_ru",
        )

    def get_fields(self):
        fields = super().get_fields()
        request_method = (
                self.context.get("request", None) and self.context["request"].method
        )

        if request_method and request_method not in ["GET"]:
            fields.pop("product", None)

        return fields



    # def get_fields(self):
    #     fields = super().get_fields()
    #     request_method = self.context["request"].method
    #     # if request_method in ["GET"]:
    #     #     fields.pop("product", None)
    #     # if request_method not in ["GET"]:
    #     #     fields.pop("product", None)
    #     return fields


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            "id",
            "title_uz",
            "title_ru",
        )


class MainPageCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "is_index",
            "image",
        )


class IndexCategorySerializer(ModelSerializer):
    class Meta:
        model = IndexCategory
        fields = (
            "id",
            "title_uz",  # noqa
            "title_ru",  # noqa
            "image",
            "category",
            "sub_category",
            "brand",
            "stock",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["stock"] = self.get_stock(instance)

        if self.context["request"].method == "POST":
            data["category"] = (
                {"id": instance.category.id, "title": instance.category.title}
                if instance.category
                else None
            )
            data["sub_category"] = (
                {"id": instance.sub_category.id, "title": instance.sub_category.title}
                if instance.sub_category
                else None
            )
            data["brand"] = (
                {"id": instance.brand.id, "title": instance.brand.title}
                if instance.brand
                else None
            )
        else:
            data["category"] = (
                {"id": instance.category.id, "title": instance.category.title}
                if instance.category
                else None
            )
            data["sub_category"] = (
                {"id": instance.sub_category.id, "title": instance.sub_category.title}
                if instance.sub_category
                else None
            )
            data["brand"] = (
                {"id": instance.brand.id, "title": instance.brand.title}
                if instance.brand
                else None
            )

        return data

    @staticmethod
    def get_category(obj):
        category = obj.category
        if category:
            return {"id": category.id, "title": category.title}
        return None

    @staticmethod
    def get_sub_category(obj):
        sub_category = obj.sub_category
        if sub_category:
            return {"id": sub_category.id, "title": sub_category.title}
        return None

    @staticmethod
    def get_brand(obj):
        brand = obj.brand
        if brand:
            return {"id": brand.id, "title": brand.title}
        return None

    @staticmethod
    def get_stock(obj):
        stock = obj.stock
        if stock:
            return {"id": stock.id, "stock_type": stock.title}
        return None


class ProductSearchSerializer(ModelSerializer):
    sub_categories = SerializerMethodField()
    categories = SerializerMethodField()
    brands = SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "price",
            "sales",
            "categories",
            "sub_categories",
            "brands",
            "image",
            "slug",
        )

    @staticmethod
    def get_sub_categories(obj: Product) -> Optional[Dict[str, str]]:
        sub_category = getattr(obj, "sub_category", None)
        if sub_category:
            return {
                "id": sub_category.id,
                "title_uz": sub_category.title_uz,
                "title_ru": sub_category.title_ru,
            }
        else:
            raise ValueError("Sub-category is not available.")

    @staticmethod
    def get_brands(obj: Product) -> Optional[Dict[str, str]]:
        brand = getattr(obj, "brand", None)
        if brand:
            return {
                "id": brand.id,
                "title_uz": brand.title_uz,
                "title_ru": brand.title_ru,
            }
        else:
            raise ValueError("Brand is not available.")

    @staticmethod
    def get_categories(obj: Product) -> Optional[Dict[str, str]]:
        category = getattr(obj, "category", None)
        if category:
            return {
                "id": category.id,
                "title_uz": category.title_uz,
                "title_ru": category.title_ru,
            }
        else:
            raise ValueError("Category is not available.")

    def get_image(self, instance: "Product") -> Dict[str, Any]:
        request = self.context.get("request")
        first_image = instance.images.first()

        if first_image:
            image_url = request.build_absolute_uri(first_image.image.url)
            return {"id": first_image.id, "image": image_url}
        else:
            return {"id": None, "image": None}


class ProductSerializer(SymbolValidationMixin, ModelSerializer):
    sub_categories = SerializerMethodField()
    categories = SerializerMethodField()
    index_categories = SerializerMethodField()
    brands = SerializerMethodField()
    images = SerializerMethodField()
    image_ids = ListField(
        write_only=True,
        child=PrimaryKeyRelatedField(queryset=Images.objects.all()),
        required=False,
    )
    short_descriptions = ShortDescriptionSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "price",
            "sales",
            "category",
            "categories",
            "stock",
            "images",
            "image_ids",
            "description_uz",
            "description_ru",
            "is_available",
            "sub_category",
            "brand",
            "index_category",
            "index_categories",
            "brands",
            "sub_categories",
            "short_descriptions",
            "created_at",
            "slug",
        )

    def create(self, validated_data):
        image_ids = validated_data.pop("image_ids", [])
        short_descriptions_data = validated_data.pop("short_descriptions", [])

        product = Product.objects.create(**validated_data)

        product.images.set(image_ids)

        for short_description_data in short_descriptions_data:
            ShortDescription.objects.create(product=product, **short_description_data)

        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.images.set(validated_data.pop("image_ids", []))

        # Update simple fields
        instance.title_uz = validated_data.get("title_uz", instance.title_uz)
        instance.title_ru = validated_data.get("title_ru", instance.title_ru)
        instance.price = validated_data.get("price", instance.price)
        instance.sales = validated_data.get("sales", instance.sales)
        instance.description_uz = validated_data.get("description_uz", instance.description_uz)
        instance.description_ru = validated_data.get("description_ru", instance.description_ru)
        instance.is_available = validated_data.get("is_available", instance.is_available)
        instance.sub_category = validated_data.get("sub_category", instance.sub_category)
        instance.brand = validated_data.get("brand", instance.brand)
        instance.stock = validated_data.get("stock", instance.stock)

        # Update or create short_descriptions
        short_descriptions_data = validated_data.pop("short_descriptions", [])
        instance.short_descriptions.all().delete()
        for short_description_data in short_descriptions_data:
            ShortDescription.objects.create(product=instance, **short_description_data)


        # Update index_category
        index_category_data = validated_data.get("index_category")
        index_category_instance = instance.index_category

        if index_category_data is not None:
            index_category_instance = IndexCategory.objects.get(id=index_category_data.id)
        elif index_category_instance:
            index_category_instance.delete()
            instance.index_category = None

        if index_category_instance:
            instance.index_category = index_category_instance

        instance.save()

        # Refresh from DB to get the updated values
        instance.refresh_from_db()

        return instance

    @staticmethod
    def get_related_products(instance):
        sub_category = instance.sub_category
        if sub_category:
            category = sub_category.category
            if category:
                related_products = Product.objects.filter(
                    sub_category__category=category
                ).exclude(id=instance.id)
                return related_products
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        related_products = self.get_related_products(instance)

        if related_products is not None:
            related_products_data = [
                {
                    "id": product.id,
                    "title_uz": product.title_uz,
                    "title_ru": product.title_ru,
                    "images": self.get_images(product),
                    "price": product.price,
                    "sales": product.sales,
                    "slug": product.slug,
                    "short_descriptions": ShortDescriptionSerializer(
                        product.short_descriptions, many=True
                    ).data,
                }
                for product in related_products
            ]
            short_descriptions_data = ShortDescriptionSerializer(
                instance.short_descriptions.all(), many=True
            ).data
            representation["short_descriptions"] = short_descriptions_data

            representation["related_products"] = related_products_data
            representation["stock"] = self.get_stock(instance)
            request_method = self.context["request"].method
            if request_method != "GET":
                representation.pop("created_at", None)

        return representation

    @staticmethod
    def get_stock(obj):
        stock = obj.stock
        if stock:
            return {"id": stock.id, "stock_type": stock.title}
        return None

    def get_images(self, instance: "Product") -> List[Dict[str, Any]]:
        request = self.context.get("request")

        if request:
            images_data = instance.images.all()
            serialized_images = []

            for image in images_data:
                image_url = request.build_absolute_uri(image.image.url)
                serialized_images.append({"id": image.id, "image": image_url})

            return serialized_images
        else:
            return []

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context["request"].method
        if request_method not in ["GET"]:
            fields.pop("slug", None)
        if request_method in ["GET"]:
            fields.pop("sub_category", None)
        if request_method in ["GET"]:
            fields.pop("brand", None)
        if request_method in ["GET"]:
            fields.pop("category", None)
        if request_method in ["GET"]:
            fields.pop("index_category", None)
        return fields

    @staticmethod
    def get_sub_categories(obj: Product) -> Optional[Dict[str, str]]:
        sub_category = getattr(obj, "sub_category", None)
        if sub_category:
            return {
                "id": sub_category.id,
                "title_uz": sub_category.title_uz,
                "title_ru": sub_category.title_ru,
            }
        else:
            raise ValueError("Sub-category is not available.")

    @staticmethod
    def get_brands(obj: Product) -> Optional[Dict[str, str]]:
        brand = getattr(obj, "brand", None)
        if brand:
            return {
                "id": brand.id,
                "title_uz": brand.title_uz,
                "title_ru": brand.title_ru,
            }
        else:
            raise ValueError("Brand is not available.")

    @staticmethod
    def get_categories(obj: Product) -> Optional[Dict[str, str]]:
        category = getattr(obj, "category", None)
        if category:
            return {
                "id": category.id,
                "title_uz": category.title_uz,
                "title_ru": category.title_ru,
            }
        else:
            raise ValueError("Category is not available.")

    @staticmethod
    def get_index_categories(obj: Product) -> Optional[Dict[str, str]]:
        index_category = getattr(obj, "index_category", None)
        if index_category:
            return {
                "id": getattr(index_category, "id", None),
                "title_uz": getattr(index_category, "title_uz", None),
                "title_ru": getattr(index_category, "title_ru", None),
            }
        else:
            return None


class ProductCatalogSerializer(ModelSerializer):
    images = SerializerMethodField()
    stock = StockSerializer()
    brand = SerializerMethodField()
    short_descriptions = ShortDescriptionSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "price",
            "sales",
            "brand",
            "stock",
            "images",
            "short_descriptions",
            "slug",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        short_descriptions_data = ShortDescriptionSerializer(
            instance.short_descriptions.all(), many=True
        ).data
        representation["short_descriptions"] = short_descriptions_data

        return representation

    def get_brand(self, instance: "Product") -> str:
        return instance.brand.title

    def get_images(self, instance: "Product") -> List[Dict[str, Any]]:
        request = self.context.get("request")  # noqa
        images_data = instance.images.all()
        serialized_images = []

        for image in images_data:
            image_url = request.build_absolute_uri(image.image.url)
            serialized_images.append({"id": image.id, "image": image_url})

        return serialized_images


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = (
            "id",
            "web_image_uz",  # noqa
            "web_image_ru",  # noqa
            "rsp_image_uz",  # noqa
            "rsp_image_ru",  # noqa
            "is_advertisement",
            "category",
            "sub_category",
            "brand",
            "product",
            "stock",
        )

    def update(self, instance, validated_data):
        stock_data = validated_data.pop("stock", None)

        if stock_data and isinstance(stock_data, dict):
            stock_instance = Stock.objects.get(id=stock_data.get("id"))
            instance.stock = stock_instance

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["stock"] = self.get_stock(instance)
        if self.context["request"].method == "POST":
            data["category"] = instance.category.id if instance.category else None
            data["sub_category"] = (
                instance.sub_category.id if instance.sub_category else None
            )
            data["brand"] = instance.brand.id if instance.brand else None
            data["product"] = instance.product.id if instance.product else None
        else:
            data["category"] = self.get_category(instance)
            data["sub_category"] = self.get_sub_category(instance)
            data["brand"] = self.get_brand(instance)
            data["product"] = self.get_product(instance)

        return data

    def get_stock(self, obj):
        stock = obj.stock
        if stock:
            return {"id": stock.id, "stock_type": stock.title}
        return None

    def get_category(self, obj):
        category = obj.category
        if category:
            return {
                "id": category.id,
                "title_uz": category.title_uz,
                "title_ru": category.title_ru,
            }
        return None

    def get_sub_category(self, obj):
        sub_category = obj.sub_category
        if sub_category:
            return {
                "id": sub_category.id,
                "title_uz": sub_category.title_uz,
                "title_ru": sub_category.title_ru,
            }
        return None

    def get_brand(self, obj):
        brand = obj.brand
        if brand:
            return {
                "id": brand.id,
                "title_uz": brand.title_uz,
                "title_ru": brand.title_ru,
            }
        return None

    def get_product(self, obj):
        product = obj.product
        if product:
            return {"id": product.id, "title": product.title}
        return None


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "product_id",
            "title",
            "price",
            "sales",
            "count",
            "product_title",
            "created_at",
        )

    title = serializers.CharField(source="product_id.title", read_only=True)
    price = serializers.IntegerField(source="product_id.price", read_only=True)
    sales = serializers.IntegerField(source="product_id.sales", read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["created_at"] = instance.created_at.strftime("%Y-%m-%d")

        return representation

    def get_fields(self):
        fields = super().get_fields()
        request_method = (
                self.context.get("request", None) and self.context["request"].method
        )

        if request_method and request_method in ["POST"]:
            fields.pop("product_title", None)

        return fields


class OrderUserSerializer(ModelSerializer):
    order = OrderSerializer(many=True, required=False)

    class Meta:
        model = OrderUser
        fields = ("name", "phone", "address", "order", "created_at")

    def create(self, validated_data):
        order_data = validated_data.pop("order", [])
        order_user = OrderUser.objects.create(**validated_data)
        for order_item_data in order_data:
            order_item_data["order"] = order_user
            Order.objects.create(**order_item_data)
        return order_user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = OrderSerializer(
            instance.user_order.all(), many=True
        ).data

        representation["created_at"] = instance.created_at.strftime("%Y-%m-%d")

        return representation


class OrderUserGetSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=True, required=False)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderUser
        fields = (
            "id",
            "name",
            "phone",
            "address",
            "order",
            "total_price",
            "created_at",
        )

    def create(self, validated_data):
        order_data = validated_data.pop("order", [])
        order_user = OrderUser.objects.create(**validated_data)
        total_price = 0

        for order_item_data in order_data:
            order_item_data["order"] = order_user
            order = Order.objects.create(**order_item_data)

            if order.product_id.sales is not None:
                total_price += order.product_id.sales * order.count
            else:
                total_price += order.product_id.price * order.count

        order_user.total_price = total_price
        order_user.save()

        return order_user

    def get_total_price(self, instance) -> float:
        return instance.total_price

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = OrderSerializer(
            instance.user_order.all(), many=True
        ).data

        representation["created_at"] = instance.created_at.strftime("%Y-%m-%d")

        return representation
