from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'hometown',
        'latitude', 
        'longitude', 
        'units',
        )  # Customize as needed


