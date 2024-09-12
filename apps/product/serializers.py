from typing import Any, Dict, List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Max, Min, Count
from rest_framework import serializers
from rest_framework.fields import ImageField, ListField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.product.models import (Banner, Category,
                                 Images, IndexCategory, Order, OrderUser,
                                 Product, ShortDescription, Stock, SubCategory)
from apps.utils import SymbolValidationMixin
from config import settings
from drf_spectacular.utils import extend_schema_field



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



class SubCategorySerializer(ModelSerializer):
    min_price = SerializerMethodField()
    max_price = SerializerMethodField()
    categories = SerializerMethodField()

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
        )


class CategoryCountSerializer(ModelSerializer):
    count = SerializerMethodField()

    @staticmethod
    def get_count(obj) -> int:
        return Category.objects.filter(is_index=True).count()

    class Meta:
        model = Category
        fields = ("count",)




class SubCategoryAllSerializer(ModelSerializer):
    min_price = SerializerMethodField()
    max_price = SerializerMethodField()

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
        )


class AllCategorySerializer(ModelSerializer):
    sub_categories = SubCategoryAllSerializer(many=True, read_only=True)

    min_price = SerializerMethodField()
    max_price = SerializerMethodField()

    # sub_categories = SerializerMethodField()


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
            "sub_categories",
        )


class CategorySerializer(ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    min_price = SerializerMethodField()
    max_price = SerializerMethodField()
    count = SerializerMethodField()

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
    def get_stock(obj):
        stock = obj.stock
        if stock:
            return {"id": stock.id, "stock_type": stock.title}
        return None

class ProductSearchSerializer(ModelSerializer):
    sub_categories = SerializerMethodField()
    categories = SerializerMethodField()
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
            "image",
            "slug",
            "gender",  # Add gender field here
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

        if (first_image):
            image_url = request.build_absolute_uri(first_image.image.url)
            return {"id": first_image.id, "image": image_url}
        else:
            return {"id": None, "image": None}


class ProductSerializer(SymbolValidationMixin, ModelSerializer):
    related_products = SerializerMethodField()
    sub_categories = SerializerMethodField()
    categories = SerializerMethodField()
    index_categories = SerializerMethodField()
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
            "index_category",
            "index_categories",
            "sub_categories",
            "short_descriptions",
            "created_at",
            "slug",
            "gender",  # Gender field added here
            "related_products",
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
        instance.stock = validated_data.get("stock", instance.stock)
        instance.gender = validated_data.get("gender", instance.gender)  # Update gender

        # Update or create short_descriptions
        short_descriptions_data = validated_data.pop("short_descriptions", [])
        instance.short_descriptions.all().delete()
        for short_description_data in short_descriptions_data:
            ShortDescription.objects.create(product=instance, **short_description_data)

        # Update index_category
        index_category_data = validated_data.get("index_category")
        if index_category_data:
            if instance.index_category:
                instance.index_category = IndexCategory.objects.update_or_create(
                    defaults=index_category_data, id=instance.index_category.id)[0]
            else:
                instance.index_category = IndexCategory.objects.create(**index_category_data)
        elif instance.index_category:
            instance.index_category.delete()
            instance.index_category = None

        instance.save()
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
    short_descriptions = ShortDescriptionSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "price",
            "sales",
            "stock",
            "images",
            "short_descriptions",
            "slug",
            "gender",  # Add gender field here
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        short_descriptions_data = ShortDescriptionSerializer(
            instance.short_descriptions.all(), many=True
        ).data
        representation["short_descriptions"] = short_descriptions_data

        return representation

    def get_images(self, instance: "Product") -> List[Dict[str, Any]]:
        request = self.context.get("request")
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
            data["product"] = instance.product.id if instance.product else None
        else:
            data["category"] = self.get_category(instance)
            data["sub_category"] = self.get_sub_category(instance)
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


    def get_product(self, obj):
        product = obj.product
        if product:
            return {"id": product.id, "title": product.title}
        return None
        
class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product_title = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("product_id", "count", "created_at", "product_title")

    @extend_schema_field(serializers.CharField())
    def get_product_title(self, instance):
        if instance.product_id is None:
            return "Unknown Product"
        return instance.product_id.title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # product_title is handled by get_product_title, so no need to adjust it here
        return representation


class OrderUserSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=True, required=False)

    class Meta:
        model = OrderUser
        fields = ("name", "phone", "address", "order", "created_at")

    def create(self, validated_data):
        order_data = validated_data.pop("order", [])
        order_user = OrderUser.objects.create(**validated_data)
        for order_item_data in order_data:
            Order.objects.create(
                order=order_user,
                product_id=order_item_data["product_id"],  # Ensure product_id is passed as an integer
                count=order_item_data["count"],
            )
        return order_user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = OrderSerializer(
            instance.user_orders.all(), many=True
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

            if order.product_id and order.product_id.sales is not None:
                total_price += order.product_id.sales * order.count
            elif order.product_id:
                total_price += order.product_id.price * order.count

        order_user.total_price = total_price
        order_user.save()

        return order_user

    def get_total_price(self, instance) -> float:
        return instance.total_price

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["order"] = OrderSerializer(
            instance.user_orders.all(), many=True
        ).data

        representation["created_at"] = instance.created_at.strftime("%Y-%m-%d")

        return representation


class OrderUserAnalyticsSerializer(serializers.ModelSerializer):
    total_sales_amount = serializers.ReadOnlyField()
    average_order_value = serializers.ReadOnlyField()
    recent_orders = serializers.SerializerMethodField()
    most_frequent_products = serializers.SerializerMethodField()
    orders_over_time = serializers.SerializerMethodField()

    class Meta:
        model = OrderUser
        fields = [
            "id",
            "name",
            "phone",
            "address",
            "total_sales_amount",
            "average_order_value",
            "recent_orders",
            "most_frequent_products",
            "orders_over_time",
        ]

    def get_recent_orders(self, obj):
        recent_orders = obj.recent_orders
        if not recent_orders:
            return []
        return OrderSerializer(recent_orders, many=True).data

    def get_most_frequent_products(self, obj):
        if obj.most_frequent_products is None:
            return []  # Or another sensible default value
        return obj.most_frequent_products

    def get_orders_over_time(self, obj):
        if obj.orders_over_time is None:
            return []  # Or another sensible default value
        return [date.strftime("%Y-%m-%d") for date in obj.orders_over_time]


class UserSalesStatisticsSerializer(serializers.ModelSerializer):
    total_spent = serializers.IntegerField()
    orders_count = serializers.IntegerField()

    class Meta:
        model = OrderUser
        fields = ('name', 'phone', 'total_spent', 'orders_count')



class CategoryStatisticsSerializer(serializers.ModelSerializer):
    sub_category_count = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('title', 'sub_category_count', 'price_range')

    @extend_schema_field(str)
    def get_sub_category_count(self, obj):
        return SubCategory.objects.filter(category=obj).count()


    @extend_schema_field(str)
    def get_price_range(self, obj):
        products = Product.objects.filter(sub_category__category=obj)
        price_range = products.aggregate(
            min_price=Min('price'),
            max_price=Max('price')
        )
        return {
            'min_price': price_range.get('min_price', 0),
            'max_price': price_range.get('max_price', 0)
        }


class ProductStatisticsSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def to_representation(self, instance):
        product_stats = Product.objects.aggregate(
            total_products=Count('id'),
            min_price=Min('price'),
            max_price=Max('price')
        )

        product_stats['min_price'] = product_stats['min_price'] or 0
        product_stats['max_price'] = product_stats['max_price'] or 0
        return product_stats


