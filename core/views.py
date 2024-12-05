from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from weatherapi.models import DailyForecast
from weatherapi.services import fetch_forecast_by_lat_lon, fetch_and_save_forecast
from datetime import date

from django.shortcuts import render

# View for handling both logged-in and non-logged-in users
def home(request):
    if request.user.is_authenticated:
        # This is the view for logged-in users
        city = None
        weather_data = None
        location = request.GET.get('location')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        if location and latitude and longitude:
            # Fetch forecast for the entered location using lat/lon
            weather_data = fetch_forecast_by_lat_lon(latitude, longitude)
            city = location
        else:
            # Fetch weather data based on user's lat/lon
            user_profile = request.user.userprofile
            latitude = user_profile.latitude
            longitude = user_profile.longitude

            if latitude and longitude:
                fetch_and_save_forecast(request.user)
                latest_forecast = DailyForecast.objects.filter(user=request.user).order_by('date')[:7]

                weather_data = [
                    {
                        'day': forecast.date,
                        'summary': forecast.summary,
                        'icon': forecast.icon,
                        'temperature_min': forecast.temperature_min,
                        'temperature_max': forecast.temperature_max,
                        'precipitation_amt': forecast.precipitation_total,
                        'precipitation_type': forecast.precipitation_type,
                        'wind_speed': forecast.wind_speed,
                    }
                    for forecast in latest_forecast
                ] if latest_forecast.exists() else None

                # Use user's hometown as the city name
                city = user_profile.hometown

        return render(request, 'core/home.html', {
            'city': city,
            'weather_data': weather_data,
        })

    else:
        # This is the view for non-logged-in users
        return render(request, 'authenticate/landing_page.html')
