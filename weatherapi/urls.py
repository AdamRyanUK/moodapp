from django.urls import path
from .views import city_autocomplete

urlpatterns = [
    path('city-autocomplete/', city_autocomplete, name='city-autocomplete'),
]
