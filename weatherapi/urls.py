from django.urls import path
from .views import nearest_place, city_autocomplete, get_hourly_forecast


urlpatterns = [
    path('city-autocomplete/', city_autocomplete, name='city-autocomplete'),
    path('hourly_forecast/', get_hourly_forecast, name='hourly_forecast'),
    path("nearest-place/", nearest_place, name="nearest-place"),
]
