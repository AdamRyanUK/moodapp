from django.contrib import admin
from .models import Profile, Location

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id', 'hometown', 'current_location', 'lat', 'lon', 'units', 'first_login')

    def user_id(self, obj):
        return obj.user.id
    user_id.short_description = 'User ID'

class LocationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'place_name', 'lat', 'lon', 'start_date', 'end_date', 'location_type')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Location, LocationAdmin)