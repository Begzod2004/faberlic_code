from django.core.exceptions import ValidationError
from django.db.models import (CASCADE, SET_NULL, BigIntegerField, BooleanField,
                              CharField, DateTimeField, ForeignKey, ImageField,
                              IntegerField, ManyToManyField, Max, Min, Model,
                              SlugField, TextField)
from rest_framework.exceptions import ValidationError
from slugify import slugify

from apps.utils import generate_unique_filename


def calculate_price_range(queryset, field_name="price"):
    prices = queryset.values_list(field_name, flat=True)
    min_price = min(prices) if prices else None
    max_price = max(prices) if prices else None

    return {
        "min_price": 0 if min_price == max_price else min_price,
        "max_price": max_price,
    }


class Category(Model):
    title = CharField(max_length=255, unique=True)
    is_index = BooleanField(default=False)
    image = ImageField(upload_to=generate_unique_filename, null=True, blank=True)

    @property
    def price_range(self):
        return calculate_price_range(self.sub_categories.all(), "price")

    @property
    def sub_category_count(self):
        return self.sub_categories.count()

    @staticmethod
    def get_all_categories_instance():
        return Category(title="All categories", id=0)


class SubCategory(Model):
    title = CharField(max_length=255, unique=True)
    category = ForeignKey(Category, on_delete=CASCADE, related_name="sub_categories")


class Images(Model):
    image = ImageField(upload_to=generate_unique_filename, null=True, blank=True)


class Stock(Model):
    title = CharField(max_length=50, null=True, blank=True)


class IndexCategory(Model):
    title = CharField(max_length=255, null=True, blank=True, unique=True)
    image = ImageField(max_length=255, upload_to=generate_unique_filename, null=True)
    category = ForeignKey(
        Category,
        on_delete=CASCADE,
        related_name="index_categories",
        null=True,
        blank=True,
    )
    sub_category = ForeignKey(
        SubCategory,
        on_delete=CASCADE,
        related_name="index_sub_categories",
        null=True,
        blank=True,
    )
    stock = ForeignKey(
        Stock, on_delete=CASCADE, related_name="index_stock", null=True, blank=True
    )

class Product(Model):
    GENDER_CHOICES = [
        ('M', 'Erkak (Male)'),
        ('F', 'Ayol (Female)'),
        ('U', 'Unisex'),
    ]

    title = CharField(max_length=255)
    price = IntegerField()
    sales = IntegerField(null=True, blank=True)
    images = ManyToManyField(Images, related_name="product_images")
    description = TextField()
    is_available = BooleanField(default=True)
    stock = ForeignKey(Stock, on_delete=CASCADE, related_name="product_stock", null=True, blank=True)
    sub_category = ForeignKey(SubCategory, on_delete=CASCADE, related_name="products")
    category = ForeignKey(Category, on_delete=CASCADE, related_name="products")
    index_category = ForeignKey(IndexCategory, on_delete=CASCADE, related_name="index_category_products", null=True, blank=True)
    slug = SlugField(max_length=255, unique=True)
    gender = CharField(max_length=1, choices=GENDER_CHOICES, default='U')

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
    if not self.pk:
        self.slug = slugify(self.title)

    while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
        if "-" in self.slug:
            parts = self.slug.split("-")
            if parts[-1].isdigit():
                count = int(parts[-1])
                self.slug = "-".join(parts[:-1]) + "-" + str(count + 1)
            else:
                self.slug += "-1"
        else:
            self.slug += "-1"

    super().save(*args, **kwargs)

    # Validate the number of images after saving
    if self.images.count() > 3:
        raise ValidationError("Cannot have more than 3 images for a product.")

        # Save the related index_category object if it exists
        # if self.index_category:
        #     self.index_category.save()  


    def clean(self):
        if self.sales and self.sales < 0:
            raise ValidationError("Sales must be a non-negative value.")
        if self.sales and self.sales > self.price:
            raise ValidationError("Sales cannot be greater than the price.")

    @property
    def discounted_price(self):
        if self.sales:
            return self.price - self.sales
        return self.price


    @property
    def min_price(self):
        return Product.objects.aggregate(Min("price"))["price__min"] or 0

    @property
    def max_price(self):
        return Product.objects.aggregate(Max("price"))["price__max"] or 0



# Banner bu >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class Banner(Model):
    web_image = ImageField(
        max_length=255, upload_to=generate_unique_filename, null=True
    )
    rsp_image = ImageField(
        max_length=255, upload_to=generate_unique_filename, null=True
    )
    is_advertisement = BooleanField(default=False)
    category = ForeignKey(
        Category,
        on_delete=CASCADE,
        related_name="banner_categories",
        null=True,
        blank=True,
    )
    sub_category = ForeignKey(
        SubCategory,
        on_delete=CASCADE,
        related_name="banner_sub_categories",
        null=True,
        blank=True,
    )
    stock = ForeignKey(
        Stock, on_delete=CASCADE, related_name="banner_stock", null=True, blank=True
    )
    product = ForeignKey(
        Product,
        on_delete=CASCADE,
        related_name="banner_products",
        null=True,
        blank=True,
    )


class ShortDescription(Model):
    key = CharField(max_length=255)
    value = CharField(max_length=255)
    product = ForeignKey(Product, on_delete=CASCADE, related_name="short_descriptions")



class OrderUser(Model):
    name = CharField(max_length=255, blank=True, null=True)
    phone = CharField(max_length=255)
    address = CharField(max_length=255, blank=True, null=True)
    total_price = BigIntegerField()
    product_title = CharField(max_length=255, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)

    @property
    def total_sales_amount(self):
        """
        Рассчитывает общую сумму продаж для пользователя заказа.

        Суммирует общие цены всех заказов, связанных с этим пользователем.

        Возвращает:
        int: Общая сумма продаж или 0, если нет заказов.
        """
        return (
            self.orders.aggregate(total_amount=Sum("total_price"))["total_amount"] or 0
        )

    @property
    def average_order_value(self):
        """
        Рассчитывает среднюю стоимость заказа для пользователя.

        Делит общую сумму всех заказов на количество заказов.

        Возвращает:
        float: Средняя стоимость заказа или 0, если нет заказов.
        """
        orders = self.orders.all()
        total_amount = (
            orders.aggregate(total_amount=Sum("total_price"))["total_amount"] or 0
        )
        total_count = orders.count()
        return total_amount / total_count if total_count > 0 else 0

    @property
    def recent_orders(self):
        """
        Возвращает последние заказы пользователя.

        Сортирует заказы по дате создания в порядке убывания.

        Возвращает:
        QuerySet: Последние 5 заказов пользователя.
        """
        return self.user_orders.order_by("-created_at")[:5]

    @property
    def most_frequent_products(self):
        """
        Получает наиболее часто заказываемые пользователем продукты.

        Возвращает список продуктов с их названиями, ценами и количеством.

        Возвращает:
        список: Список словарей с 'product_id', 'product_title', 'price' и 'count' для каждого продукта.
        """
        product_data = (
            self.user_orders.select_related("product_id")
            .values("product_id__title", "product_id__price", "product_id")
            .annotate(count=Sum("count"))
            .order_by("-count")
        )

        return [
            {
                "product_id": item["product_id"],
                "product_title": item["product_id__title"],
                "price": item["product_id__price"],
                "count": item["count"],
            }
            for item in product_data
        ]

    @property
    def orders_over_time(self):
        """
        Возвращает список дат, когда были созданы заказы, сгруппированных по месяцам.

        Возвращает:
        QuerySet: Список дат, сгруппированных по месяцам.
        """
        return self.user_orders.dates("created_at", "month")


class Order(Model):
    product_id = ForeignKey(Product, on_delete=SET_NULL, null=True, blank=True)
    product_title = CharField(max_length=255, blank=True, null=True)
    count = IntegerField(null=True, blank=True)
    # total_price = BigIntegerField()
    order = ForeignKey(OrderUser, CASCADE, related_name="user_orders")
    created_at = DateTimeField(auto_now_add=True)