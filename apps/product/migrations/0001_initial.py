# Generated by Django 4.2.11 on 2024-03-26 19:42

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='category_images', verbose_name='Rasm')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Telefon Raqami')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan Vaqti')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan Vaqti')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Qayta ishlandimi?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Buyurtma',
                'verbose_name_plural': 'Buyurtmalar',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Narxi')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_featured', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Product Kategory')),
            ],
            options={
                'verbose_name': 'MAXSULOT',
                'verbose_name_plural': 'Mahsulotlar',
                'ordering': ['-created_at'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RecCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Reccategory',
                'verbose_name_plural': 'Reccategories',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nomi', max_length=123)),
                ('star', models.IntegerField(default=0, verbose_name='star')),
                ('review_comment', models.TextField()),
                ('review_date', models.DateTimeField(auto_now_add=True, verbose_name='review_created_date')),
                ('email', models.EmailField(max_length=254)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productreview', to='product.product')),
            ],
            options={
                'verbose_name': 'Product Rating',
                'verbose_name_plural': 'Product Ratings',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='rec_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.reccategory', verbose_name='Rekamindatsiya Kategoriyasi'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Miqdori')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product.order', verbose_name='Buyurtma')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Mahsulot')),
            ],
            options={
                'verbose_name': 'Buyurtma Bandidagi Mahsulot',
                'verbose_name_plural': 'Buyurtma Bandidagi Mahsulotlar',
            },
        ),
        migrations.CreateModel(
            name='RecCategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='product.reccategory')),
            ],
            options={
                'verbose_name': 'Reccategory Translation',
                'db_table': 'product_reccategory_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=300, verbose_name='Nomi')),
                ('description', ckeditor.fields.RichTextField()),
                ('tag', models.TextField(default='Women', verbose_name='Tag')),
                ('short_description', models.CharField(blank=True, default='NEW', max_length=300, null=True)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='product.product')),
            ],
            options={
                'verbose_name': 'MAXSULOT Translation',
                'db_table': 'product_product_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', ckeditor.fields.RichTextField(default=None)),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='product.category')),
            ],
            options={
                'verbose_name': 'Category Translation',
                'db_table': 'product_category_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
