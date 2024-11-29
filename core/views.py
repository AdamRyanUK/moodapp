from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from weatherapi.services import fetch_and_save_forecast, get_forecast_for_location
from .utils import get_nearest_town
from weatherapi.models import DailyForecast

@login_required
def home(request):
    city = None
    weather_data = None
    location = request.GET.get('location')

    if location:
        # Fetch forecast for the entered location
        weather_data, city = get_forecast_for_location(location)    
    else:

        # If city is not in session, use latitude and longitude from user's profile
        if not city:
            user_profile = request.user.userprofile
            latitude = user_profile.latitude
            longitude = user_profile.longitude

            if latitude and longitude:
                city = get_nearest_town(latitude, longitude)  # Get city from lat/lon
                request.session['city'] = city  # Store city in session

        # Fetch weather data using the city from the session
        fetch_and_save_forecast(request.user)

        latest_forecast = DailyForecast.objects.filter(user=request.user).order_by('date')[:7]

        weather_data = []
        if latest_forecast.exists():
            for forecast in latest_forecast:
                weather_data.append({
                    'day': forecast.date,
                    'summary': forecast.summary,
                    'icon': forecast.icon,
                    'temperature_min': forecast.temperature_min,
                    'temperature_max': forecast.temperature_max,
                    'precipitation_amt': forecast.precipitation_total,
                    'precipitation_type': forecast.precipitation_type,
                    'wind_speed': forecast.wind_speed,
                })

    return render(request, 'core/home.html', {
        'city': city,
        'weather_data': weather_data,
    })
