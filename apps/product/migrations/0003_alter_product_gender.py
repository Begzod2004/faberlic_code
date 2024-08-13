# Generated by Django 5.0.7 on 2024-08-13 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_remove_product_brand_remove_indexcategory_brand_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="gender",
            field=models.CharField(
                choices=[
                    ("M", "Erkak (Male)"),
                    ("F", "Ayol (Female)"),
                    ("U", "Unisex"),
                ],
                default="U",
                max_length=1,
            ),
        ),
    ]
