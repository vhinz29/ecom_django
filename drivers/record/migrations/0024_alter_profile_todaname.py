# Generated by Django 5.1.4 on 2025-02-11 04:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("record", "0023_remove_todaname_zone_toda_todaname_zone_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="todaname",
            field=models.CharField(max_length=100),
        ),
    ]
