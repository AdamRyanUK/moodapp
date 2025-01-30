from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometown = models.TextField(max_length=100, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    UNIT_CHOICES = [
        ('metric', 'Metric'),
        ('us', 'US'),
        ('uk', 'UK'),
        ('ca', 'Canada'),
    ]
    units = models.CharField(max_length=10, choices=UNIT_CHOICES, default='metric')
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username