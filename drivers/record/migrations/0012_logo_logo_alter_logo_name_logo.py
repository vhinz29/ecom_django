# Generated by Django 5.1.4 on 2025-02-08 08:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("record", "0011_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="logo",
            name="logo",
            field=models.ImageField(
                blank=True, null=True, upload_to="uploads/pictures/"
            ),
        ),
        migrations.AlterField(
            model_name="logo",
            name="name_logo",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
