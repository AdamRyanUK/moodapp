from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class LocationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='location_history')
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically sets the timestamp when a new record is created
    
    def __str__(self):
        return f"{self.city} - {self.timestamp}"

