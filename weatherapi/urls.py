from django.urls import path
from .views import nearest_place, city_autocomplete, get_hourly_forecast, historical_forecast_view,weather_feedback_view


urlpatterns = [
    path('city-autocomplete/', city_autocomplete, name='city-autocomplete'),
    path('hourly_forecast/', get_hourly_forecast, name='hourly_forecast'),
    path("nearest-place/", nearest_place, name="nearest-place"),
    path('historical-forecast/', historical_forecast_view, name='historical_forecast'),
    path('weather-feedback/', weather_feedback_view, name='weather_feedback'),
]
