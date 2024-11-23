from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField  # Use JSONField for complex nested data

class DailyForecast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    summary = models.TextField(null=True, blank=True)
    weather = models.CharField(max_length=50, null=True, blank=True)
    icon = models.IntegerField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    temperature_min = models.FloatField(null=True, blank=True)
    temperature_max = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_dir = models.CharField(max_length=5, null=True, blank=True)
    wind_angle = models.FloatField(null=True, blank=True)  # Include angle
    cloud_cover = models.FloatField(null=True, blank=True)  # Total cloud cover
    precipitation_total = models.FloatField(null=True, blank=True)
    precipitation_type = models.CharField(max_length=20, null=True, blank=True)

    # Astro data
    sunrise = models.DateTimeField(null=True, blank=True)
    sunset = models.DateTimeField(null=True, blank=True)
    moon_phase = models.CharField(max_length=50, null=True, blank=True)
    moonrise = models.DateTimeField(null=True, blank=True)
    moonset = models.DateTimeField(null=True, blank=True)

    # Statistics
    stats_temperature_avg = models.FloatField(null=True, blank=True)
    stats_temperature_avg_min = models.FloatField(null=True, blank=True)
    stats_temperature_avg_max = models.FloatField(null=True, blank=True)
    stats_temperature_record_min = models.FloatField(null=True, blank=True)
    stats_temperature_record_max = models.FloatField(null=True, blank=True)
    stats_precipitation_avg = models.FloatField(null=True, blank=True)
    stats_precipitation_probability = models.FloatField(null=True, blank=True)
    stats_wind_avg_speed = models.FloatField(null=True, blank=True)
    stats_wind_avg_angle = models.FloatField(null=True, blank=True)
    stats_wind_avg_dir = models.CharField(max_length=5, null=True, blank=True)
    stats_wind_max_speed = models.FloatField(null=True, blank=True)
    stats_wind_max_gust = models.FloatField(null=True, blank=True)

    # Raw data for anything else
    raw_data = JSONField(null=True, blank=True)

    def __str__(self):
        return f"Forecast for {self.date} - {self.user.username}"
