from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'latitude', 
        'longitude', 
        'preferred_temperature_min',
        'preferred_temperature_max',
        'likes_rain',
        'sun_worshipper',
        )  # Customize as needed


