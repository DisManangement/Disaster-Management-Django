# Generated by Django 4.2.3 on 2023-08-03 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0010_cartitem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="products",
            field=models.ManyToManyField(
                blank=True, related_name="products", to="base.cartitem"
            ),
        ),
    ]