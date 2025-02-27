from django.contrib import admin
from .models import Profile, Location

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id', 'hometown', 'current_location', 'lat', 'lon', 'units', 'first_login', 'all_steps_completed')
    fields = ('user', 'hometown', 'current_location', 'lat', 'lon', 'units', 'first_login', 'weather_preferences_completed', 'hometown_registered')
    list_filter = ('units', 'first_login', 'weather_preferences_completed', 'hometown_registered')
    search_fields = ('user__username', 'hometown', 'current_location')

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

    def all_steps_completed(self, obj):
        return obj.all_steps_completed()
    all_steps_completed.short_description = 'All Steps Completed'
    all_steps_completed.boolean = True

class LocationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'place_name', 'lat', 'lon', 'start_date', 'end_date', 'location_type')

# Enregistrements uniques
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location, LocationAdmin)