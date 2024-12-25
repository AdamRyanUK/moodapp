from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from weatherapi.models import DailyForecast
from weatherapi.services import fetch_forecast_by_lat_lon, fetch_and_save_forecast
from weatherapi.moodscore import calculate_mood_score
from datetime import date as datetime_date
from datetime import date
from weatherpreferences.models import WeatherFeedback
import json

def home(request):
    if request.user.is_authenticated:
        city = None
        weather_data = None
        location = request.GET.get('location')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        if location and latitude and longitude:
            # Fetch forecast for the entered location using lat/lon
            weather_data = fetch_forecast_by_lat_lon(latitude, longitude)

            # Add mood score to the weather data for searchable forecasts
            for forecast in weather_data:
                forecast['mood_score'] = calculate_mood_score(request.user, forecast)

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
                        'mood_score': calculate_mood_score(request.user, forecast),  # Calculate mood score
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

def insights(request):
    return render(request, 'core/insights.html')

@login_required
def calendar_view(request):
    today_date = datetime_date.today()
     # Fetch the feedback data for the logged-in user
    feedback = WeatherFeedback.objects.filter(user=request.user).order_by('date')
    
    # Format feedback as { 'YYYY-MM-DD': rating }
    feedback_dict = {f.date.strftime('%Y-%m-%d'): f.rating for f in feedback}
    # Serialize the feedback dictionary to JSON
    feedback_json = json.dumps(feedback_dict)
    context = {
        'date': today_date,
        'feedback_json': feedback_json,
    }
    return render(request, 'core/calendar.html', context)
