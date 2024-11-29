# Generated by Django 5.1.3 on 2024-11-29 09:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weatherpreferences", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WeatherPreferences",
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
                    "ideal_temp_max",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "ideal_temp_min",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("rain_lover", models.BooleanField(default=False)),
                ("snow_lover", models.BooleanField(default=False)),
                ("cloud_lover", models.BooleanField(default=False)),
                ("wind", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]