import random
from faker import Faker
from django.core.management.base import BaseCommand
from apps.product.models import Category, SubCategory, Product, Stock, Images, OrderUser, Order, ShortDescription



fake_en = Faker()
fake_ru = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Clear existing data
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        Stock.objects.all().delete()
        # Images.objects.all().delete()
        OrderUser.objects.all().delete()
        Order.objects.all().delete()
        ShortDescription.objects.all().delete()

        # Seed categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                title=fake_en.word(),
                title_ru=fake_ru.word(),
                title_uz=fake_ru.word(),  # Fake Uzbek data using Russian locale
                is_index=fake_en.boolean()
            )
            categories.append(category)

        # Seed subcategories
        subcategories = []
        for _ in range(10):
            subcategory = SubCategory.objects.create(
                title=fake_en.word(),
                title_ru=fake_ru.word(),
                title_uz=fake_ru.word(),  # Fake Uzbek data using Russian locale
                category=random.choice(categories)
            )
            subcategories.append(subcategory)

        
        # Seed stock
        stocks = []
        for _ in range(10):
            stock = Stock.objects.create(
                title=fake_en.word(),
                title_ru=fake_ru.word(),
                title_uz=fake_ru.word()  # Fake Uzbek data using Russian locale
            )
            stocks.append(stock)

        # Seed products
        for _ in range(20):
            product = Product.objects.create(
                title=fake_en.word(),
                title_ru=fake_ru.word(),
                title_uz=fake_ru.word(),  # Fake Uzbek data using Russian locale
                price=random.randint(10, 1000),
                sales=random.randint(0, 100),
                description=fake_en.text(),
                description_ru=fake_ru.text(),
                description_uz=fake_ru.text(),  # Fake Uzbek data using Russian locale
                is_available=fake_en.boolean(),
                stock=random.choice(stocks),
                sub_category=random.choice(subcategories),
                category=random.choice(categories),
            )

            # Create a ShortDescription for each product
            short_description = ShortDescription.objects.create(
                product=product,
                key='example_key',
                value='This is an example short description'
            )

            existing_images = list(Images.objects.all())
            if existing_images:
                product_image = random.choice(existing_images)
                product.images.add(product_image)
            else:
                product.images.add(None)

        # Seed order users
        order_users = []
        for _ in range(5):
            order_user = OrderUser.objects.create(
                name=fake_en.name(),
                phone=fake_en.phone_number(),
                address=fake_en.address(),
                total_price=random.randint(100, 5000),
                product_title=fake_en.word()
            )
            order_users.append(order_user)

        # Seed orders
        for _ in range(20):
            order = Order.objects.create(
                products=random.choice(Product.objects.all()),
                product_id=random.choice(Product.objects.all()),
                product_title=fake_en.word(),
                count=random.randint(1, 10),
                order=random.choice(order_users)
            )

        self.stdout.write(self.style.SUCCESS("Data seeding completed!"))
