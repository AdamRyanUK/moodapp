from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CitySearch 
from weatherapi.models import DailyForecast
from weatherapi.services import fetch_forecast_by_lat_lon, fetch_and_save_forecast
from weatherapi.moodscore import calculate_mood_score
from datetime import date as datetime_date
from datetime import date
from weatherpreferences.models import WeatherFeedback
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from core.feedbackanomaly.anomaly_calculations import fetch_anomaly_data

def home(request):
    if request.user.is_authenticated:
        city = None
        city_first_part = None
        weather_data = None
        location = request.GET.get('location')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        # Fetch the user profile once
        user_profile = request.user.userprofile

        if location and latitude and longitude:
            # Fetch forecast for the entered location using lat/lon
            weather_data = fetch_forecast_by_lat_lon(latitude, longitude, request.user)

            # Add mood score to the weather data for searchable forecasts
            for forecast in weather_data:
                forecast['mood_score'] = calculate_mood_score(request.user, forecast)

            # Extract the first part of the city name (before any comma)
            city = location
            city_first_part = location.split(',')[0] if ',' in location else location

            # Track the city search for the user
            if location != user_profile.hometown or (
                latitude != str(user_profile.latitude)
                and longitude != str(user_profile.longitude)
            ):
                city_search, created = CitySearch.objects.get_or_create(
                    city=location,
                    latitude=latitude,
                    longitude=longitude,
                    user=request.user  # Associate with the user
                )
                city_search.search_count += 1
                city_search.save()
        else:
            # Use user's profile latitude and longitude if no location is provided
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
                        'sunrise': forecast.sunrise,
                        'sunset': forecast.sunset,
                        'day_length': forecast.day_length,
                        'mood_score': calculate_mood_score(request.user, forecast),  # Calculate mood score
                    }
                    for forecast in latest_forecast
                ] if latest_forecast.exists() else None

                # Use user's hometown as the city name if no location is provided
                city = user_profile.hometown
                city_first_part = city.split(',')[0] if ',' in city else city

        # Extract sunrise and sunset for the first day
        first_day_sunrise = weather_data[0]['sunrise'] if weather_data else None
        first_day_sunset = weather_data[0]['sunset'] if weather_data else None
        first_day_length = weather_data[0]['day_length'] if weather_data else None

        # Query the most selected cities by the current user
        most_selected_cities = CitySearch.objects.filter(user=request.user).order_by('-search_count')[:10]

        # Add city_first_part to most_selected_cities for easy template rendering
        for city_search in most_selected_cities:
            city_search.city_first_part = city_search.city.split(',')[0] if ',' in city_search.city else city_search.city

        return render(request, 'core/home.html', {
            'city_first_part': city_first_part,
            'city': city,
            'weather_data': weather_data,
            'first_day_sunrise': first_day_sunrise,
            'first_day_sunset': first_day_sunset,
            'first_day_length': first_day_length,
            'most_selected_cities': most_selected_cities,
        })

    else:
        # This is the view for non-logged-in users
        return render(request, 'authenticate/landing_page.html')


@csrf_exempt
def remove_city(request, city_id):
    try:
        city = CitySearch.objects.get(id=city_id)
        city.delete()
        return JsonResponse({'success': True})
    except CitySearch.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'City not found.'})


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

@login_required
def feedback_anomaly_data(request):
    range = request.GET.get('range', '7d')
    user = request.user

    # Determine the date range for the query
    if range == '7d':
        start_date = timezone.now() - timedelta(days=7)
    elif range == '1m':
        start_date = timezone.now() - timedelta(days=30)
    elif range == '6m':
        start_date = timezone.now() - timedelta(days=182)
    elif range == '1y':
        start_date = timezone.now() - timedelta(days=365)
    else:
        start_date = timezone.now() - timedelta(days=7)  # Default to 7 days

    end_date = timezone.now()

    data = fetch_anomaly_data(user, start_date, end_date)

    return JsonResponse(data)

@login_required
def feedback_chart_data(request):
    range = request.GET.get('range', '7d')
    user = request.user

    # Determine the date range for the query
    if range == '7d':
        start_date = timezone.now() - timedelta(days=7)
    elif range == '1m':
        start_date = timezone.now() - timedelta(days=30)
    elif range == '6m':
        start_date = timezone.now() - timedelta(days=182)
    elif range == '1y':
        start_date = timezone.now() - timedelta(days=365)
    else:
        start_date = timezone.now() - timedelta(days=7)  # Default to 7 days

    end_date = timezone.now()
    feedbacks = WeatherFeedback.objects.filter(user=user, date__range=(start_date, end_date)).order_by('date')

    dates = [feedback.date for feedback in feedbacks]
    ratings = [feedback.rating for feedback in feedbacks]

    data = {
        'dates': dates,
        'ratings': ratings,
    }

    return JsonResponse(data)

