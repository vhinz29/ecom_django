# Generated by Django 5.1.4 on 2025-03-25 17:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("information", "0019_alter_aprs_2025_ot_approved_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="ot_approved_time",
            field=models.CharField(blank=True, default="hr", max_length=30, null=True),
        ),
    ]
