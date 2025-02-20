from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometown = models.TextField(max_length=100, blank=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)  # Current location (if different from hometown)
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
    weather_preferences_completed = models.BooleanField(default=False)
    hometown_registered = models.BooleanField(default=False)

    def all_steps_completed(self):
        return self.weather_preferences_completed and self.hometown_registered

    def __str__(self):
        return self.user.username
    
from django.db import models

class Location(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='locations')
    place_name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    lon = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    LOCATION_TYPE_CHOICES = [
        ('vacation', 'Vacation'),
        ('hometown', 'Hometown')
    ]
    location_type = models.CharField(max_length=10, choices=LOCATION_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.place_name} - From: {self.start_date} to {self.end_date}"

    class Meta:
        ordering = ['start_date']