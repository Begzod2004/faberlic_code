from django.db.models import Q
from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter
from django_filters import rest_framework as filters
from apps.product.models import Product
from django_filters import FilterSet, CharFilter, NumberFilter, OrderingFilter
from django.db.models import Q
from apps.product.models import Product, OrderUser

class ProductFilter(FilterSet):
    category = CharFilter(method="filter_category_title")
    index_category = CharFilter(method="filter_index_category_title")
    sub_category = CharFilter(method="filter_sub_category_title")
    stock = CharFilter(method="filter_stock")
    has_sale = CharFilter(method="filter_has_sale")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    is_new = CharFilter(method="filter_is_new")
    gender = CharFilter(method="filter_gender")
    order_by = OrderingFilter(
        fields=(
            ("price", "price"),
            ("title_ru", "title_ru"),
            ("title_uz", "title_uz"),
        ),
        field_labels={
            "price": "Самая высокая цена",
            "-price": "Самая низкая цена",
            "title_uz": "По алфавиту title_uz A-Z",
            "-title": "По алфавиту title_uz Z-A",
            "title_ru": "По алфавиту title_ru A-Z",
            "-title_ru": "По алфавиту title_uz Z-A",
        },
    )

    @staticmethod
    def filter_gender(queryset, name, value):
        gender_map = {
            'male': 'M', 'erkak': 'M',
            'female': 'F', 'ayol': 'F',
            'unisex': 'U'
        }
        gender_code = gender_map.get(value.lower(), None)
        print(f"Received gender value: {value}, Mapped gender code: {gender_code}")  # Debug line
        if gender_code:
            return queryset.filter(gender=gender_code)
        return queryset

    @staticmethod
    def filter_category_title(queryset, name, value):
        categories = value.split(",")
        category_filters = Q()
        for category in categories:
            category_filters |= Q(
                sub_category__category__title_ru__icontains=category
            ) | Q(sub_category__category__title_uz__icontains=category)
        return queryset.filter(category_filters)

    @staticmethod
    def filter_index_category_title(queryset, name, value):
        index_categories = value.split(",")
        index_category_filters = Q()
        for index_category in index_categories:
            index_category_filters |= Q(
                index_category__title_uz__icontains=index_category
            ) | Q(index_category__title_ru__icontains=index_category)
        return queryset.filter(index_category_filters)

    @staticmethod
    def filter_sub_category_title(queryset, name, value):
        sub_categories = value.split(",")
        sub_category_filters = Q()
        for sub_category in sub_categories:
            sub_category_filters |= Q(
                sub_category__title_ru__icontains=sub_category
            ) | Q(sub_category__title_uz__icontains=sub_category)
        return queryset.filter(sub_category_filters)

    @staticmethod
    def filter_stock(queryset, name, value):
        return queryset.filter(stock__title=value)

    @staticmethod
    def filter_has_sale(queryset, name, value):
        return (
            queryset.filter(sales=0)
            if value.lower() == "false"
            else queryset.exclude(sales=0)
        )

    @staticmethod
    def filter_is_new(queryset, name, value):
        if value.lower() == "new":
            return queryset.order_by("-id")
        return queryset

    class Meta:
        model = Product
        fields = [
            "category",
            "sub_category",
            "index_category",
            "stock",
            "min_price",
            "max_price",
            "title",
            "has_sale",
            "is_new",
            "gender",
            "order_by",
        ]

    # Existing filter methods...

    class Meta:
        model = Product
        fields = [
            "category",
            "sub_category",
            "index_category",
            "stock",
            "min_price",
            "max_price",
            "title",
            "has_sale",
            "is_new",
            "gender",
            "order_by",
        ]


class ProductSearchFilter(FilterSet):
    class Meta:
        model = Product
        fields = []


class OrderUserFilter(filters.FilterSet):
    class Meta:
        model = OrderUser
        fields = {
            "name": ["exact", "icontains"],
            "phone": ["exact"],
            "created_at": ["year", "month", "day"],
            # Add other fields as necessary
        }
