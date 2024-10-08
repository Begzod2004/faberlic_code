# Generated by Django 5.0.7 on 2024-09-05 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_alter_order_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="product.product",
            ),
            preserve_default=False,
        ),
    ]
