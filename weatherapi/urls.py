from django.urls import path
from .views import city_autocomplete, get_hourly_forecast

urlpatterns = [
    path('city-autocomplete/', city_autocomplete, name='city-autocomplete'),
    path('hourly_forecast/', get_hourly_forecast, name='hourly_forecast'),
]
