# Generated by Django 4.2.3 on 2023-08-01 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_needs_state_committee"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="needs",
            options={"ordering": ["-updated", "-created"]},
        ),
    ]
