from django.contrib import admin
from .models import HealthConditions, WeatherPreferences, JournalEntry, UserActions

class HealthConditionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'sad', 'joint_pain_arthritis')
    search_fields = ('user__username',)

class WeatherPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'ideal_temp_min', 'ideal_temp_max', 'rain_lover', 'snow_lover', 'sun_lover', 'wind_hater', 'date_updated')
    search_fields = ('user__username',)

# Register your models here
admin.site.register(HealthConditions, HealthConditionsAdmin)
admin.site.register(WeatherPreferences, WeatherPreferencesAdmin)
