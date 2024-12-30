from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class DailyForecast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dailyforecasts')
    date = models.DateField()
    summary = models.TextField(null=True, blank=True)
    weather = models.CharField(max_length=50, null=True, blank=True)
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
    sunrise = models.DateTimeField(null=True, blank=True)
    sunset = models.DateTimeField(null=True, blank=True)
    day_length = models.DurationField(null=True, blank=True)
    moon_phase = models.CharField(max_length=50, null=True, blank=True)
    moonrise = models.DateTimeField(null=True, blank=True)
    moonset = models.DateTimeField(null=True, blank=True)
    stats_temperature_avg = models.FloatField(null=True, blank=True)
    stats_temperature_avg_min = models.FloatField(null=True, blank=True)
    stats_temperature_avg_max = models.FloatField(null=True, blank=True)
    stats_temperature_record_min = models.FloatField(null=True, blank=True)
    stats_temperature_record_max = models.FloatField(null=True, blank=True)
    stats_precipitation_avg = models.FloatField(null=True, blank=True)
    stats_precipitation_probability = models.FloatField(null=True, blank=True)
    stats_wind_avg_speed = models.FloatField(null=True, blank=True)
    stats_wind_avg_angle = models.IntegerField(null=True, blank=True)
    stats_wind_avg_dir = models.CharField(max_length=10, null=True, blank=True)
    stats_wind_max_speed = models.FloatField(null=True, blank=True)
    stats_wind_max_gust = models.FloatField(null=True, blank=True)
    raw_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date}"
    
class HistoricalForecast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_generated = models.DateField(auto_now_add=True)  # Both initialization and base date
    forecasts = models.ManyToManyField(DailyForecast)  # Links to multiple daily forecasts

    def __str__(self):
        return f"Forecast for {self.user} on {self.date_generated}"


