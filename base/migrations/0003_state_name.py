# Generated by Django 4.2.3 on 2023-07-24 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_delete_login_remove_state_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="state",
            name="name",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
