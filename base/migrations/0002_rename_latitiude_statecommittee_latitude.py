# Generated by Django 4.2.3 on 2023-07-31 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="statecommittee",
            old_name="latitiude",
            new_name="latitude",
        ),
    ]