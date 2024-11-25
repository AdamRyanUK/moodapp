# In yourapp/urls.py
from django.urls import path
from .views import display_forecast, forecast_table

urlpatterns = [
    path('display-forecast/', display_forecast, name='display_forecast'),
    path('forecast-table/', forecast_table, name='forecast_table'),
]
