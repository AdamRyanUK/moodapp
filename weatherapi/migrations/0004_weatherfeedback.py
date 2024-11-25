# Generated by Django 5.1.3 on 2024-11-25 09:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weatherapi", "0003_alter_dailyforecast_cloud_cover_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WeatherFeedback",
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
                ("date", models.DateField()),
                (
                    "rating",
                    models.IntegerField(
                        choices=[
                            (1, "Very Bad"),
                            (2, "Bad"),
                            (3, "Neutral"),
                            (4, "Good"),
                            (5, "Very Good"),
                        ]
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "date")},
            },
        ),
    ]
