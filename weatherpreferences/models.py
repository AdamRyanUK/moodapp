from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class HealthConditions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sad = models.BooleanField(default=False)
    joint_pain_arthritis = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s health conditions"

class WeatherPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ideal_temp_max = models.CharField(max_length=50, null=True, blank=True)
    ideal_temp_min = models.CharField(max_length=50, null=True, blank=True)
    rain_lover = models.BooleanField(default=False)
    snow_lover = models.BooleanField(default=False)
    sun_lover = models.BooleanField(default=False)
    wind_hater = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s weather preferences"

class WeatherFeedback(models.Model):
    user = models.ForeignKey(User, related_name='weatherpreferences_feedback', on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.IntegerField(choices=[(1, 'Very Bad'), (2, 'Bad'), (3, 'Neutral'), (4, 'Good'), (5, 'Very Good')])
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    icon = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    temperature_min = models.FloatField(null=True, blank=True)
    temperature_max = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_dir = models.CharField(max_length=10, null=True, blank=True)
    wind_angle = models.IntegerField(null=True, blank=True)
    cloud_cover = models.IntegerField(null=True, blank=True)
    precipitation_total = models.FloatField(null=True, blank=True)
    precipitation_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"


