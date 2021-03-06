# Generated by Django 3.2.3 on 2021-05-26 04:51

import baronbale_website.banner_parser.generators.ticket_id_generator
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BannerCache",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gc_code", models.CharField(max_length=10)),
                ("image_url", models.CharField(blank=True, max_length=1024, null=True)),
                ("reason", models.CharField(max_length=100)),
                ("permanent", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="BannerDimension",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gc_code", models.CharField(max_length=20)),
                ("banner", models.CharField(max_length=64)),
                ("url", models.CharField(max_length=1024)),
                ("ratio", models.FloatField(default=0.0)),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="BannerParserJob",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ticket_id",
                    models.CharField(
                        default=baronbale_website.banner_parser.generators.ticket_id_generator.generate_ticket_id,
                        max_length=20,
                    ),
                ),
                (
                    "email_address_to_notify",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "uploaded_file",
                    models.FileField(
                        upload_to="", verbose_name="GPX-File or Zip Archive"
                    ),
                ),
                (
                    "horizontal_banners_per_row",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "vertical_banners_per_row",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                ("result", models.TextField(blank=True, null=True)),
                (
                    "actively_working_on_since",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("time_finished", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
