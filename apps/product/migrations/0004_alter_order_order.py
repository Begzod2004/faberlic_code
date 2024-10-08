# Generated by Django 5.0.7 on 2024-08-20 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_alter_product_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_orders",
                to="product.orderuser",
            ),
        ),
    ]
