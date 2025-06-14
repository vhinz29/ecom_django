# Generated by Django 5.1.4 on 2025-03-23 22:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "information",
            "0017_augs_2025_decs_2025_jans_2025_julys_2025_junes_2025_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="aprs_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="aprs_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="aprs_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="aprs_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="attendance",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="attendance",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="attendance",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="attendance",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="augs_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="augs_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="augs_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="augs_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="decs_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="decs_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="decs_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="decs_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="febs_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="febs_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="febs_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="febs_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="jans_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="jans_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="jans_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="jans_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="julys_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="julys_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="julys_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="julys_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="junes_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="junes_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="junes_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="junes_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="mays_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="mays_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="mays_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="mays_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="novs_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="novs_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="novs_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="novs_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="octs_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="octs_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="octs_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="octs_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="septs_2025",
            name="ot_approved",
            field=models.BooleanField(default=False, verbose_name="ot_approval"),
        ),
        migrations.AddField(
            model_name="septs_2025",
            name="ot_approved_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="septs_2025",
            name="ot_request",
            field=models.BooleanField(default=False, verbose_name="ot_requested"),
        ),
        migrations.AddField(
            model_name="septs_2025",
            name="ot_request_time",
            field=models.TimeField(blank=True, max_length=30, null=True),
        ),
    ]
