# Generated by Django 5.1.4 on 2025-02-08 14:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("record", "0015_profile_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="user",
        ),
    ]
