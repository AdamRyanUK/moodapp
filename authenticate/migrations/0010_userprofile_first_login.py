# Generated by Django 5.1.3 on 2025-01-15 19:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authenticate", "0009_remove_userprofile_is_first_login_userprofile_units"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="first_login",
            field=models.BooleanField(default=True),
        ),
    ]
