from django.shortcuts import render
import requests

def display_forecast(request):
    # Sample coordinates for demonstration
    latitude = 38.5281022
    longitude = 0.1653208

    api_key = "d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici"
    url = f"https://www.meteosource.com/api/v1/startup/point"
    params = {
        'lat': latitude,
        'lon': longitude,
        'sections': 'daily',
        'language': 'en',
        'units': 'auto',
        'key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
    except requests.RequestException as e:
        data = {"error": str(e)}

    return render(request, 'weatherapi/display_forecast.html', {'data': data})

from django.shortcuts import render
from .models import DailyForecast
from django.contrib.auth.decorators import login_required

@login_required
def forecast_table(request):
    # Fetch the latest forecast data for the logged-in user
    forecasts = DailyForecast.objects.filter(user=request.user).order_by('date')

    return render(request, 'weatherapi/forecast_table.html', {'forecasts': forecasts})
