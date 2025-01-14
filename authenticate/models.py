from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometown = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    UNIT_CHOICES = [
        ('metric', 'Metric'),
        ('us', 'US'),
        ('uk', 'UK'),
        ('ca', 'Canada'),
    ]

    units = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='metric',  # Set a default value
    )

    def __str__(self):
        return self.user.username

    