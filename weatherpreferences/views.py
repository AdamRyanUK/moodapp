import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WeatherFeedback, HealthConditions, WeatherPreferences
from .forms import UserActionsForm, JournalEntryForm, WeatherPreferencesForm, HealthConditionsForm
from weatherapi.services import fetch_forecast_by_lat_lon
from authenticate.models import Profile

@csrf_exempt  # Add this to bypass CSRF for API calls (be mindful of CSRF security in production)
@login_required
def update_location(request):
    if request.method == 'POST':
        # Parse the latitude and longitude from the incoming request
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            # Save the location to the user's profile
            user_profile, created = Profile.objects.get_or_create(user=request.user)
            user_profile.latitude = latitude
            user_profile.longitude = longitude
            user_profile.save()

            return JsonResponse({'status': 'success', 'message': 'Location updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def location_history(request):

    # Get the user's location history
    history = LocationHistory.objects.filter(user=request.user).order_by('-timestamp')
    
    return render(request, 'weatherpreferences/location_history.html', {
        'history': history,
    })

import logging

logger = logging.getLogger('django')

def parseCoordinate(coord):
    try:
        value = float(coord)
        if 'S' in coord or 'W' in coord:
            return -value
        return value
    except (ValueError, TypeError):
        return None
    
@login_required
def register_weather_preferences(request):
    if request.method == 'POST':
        weather_preferences_form = WeatherPreferencesForm(request.POST)
        health_conditions_form = HealthConditionsForm(request.POST)

        if weather_preferences_form.is_valid() and health_conditions_form.is_valid():
            weather_preferences = weather_preferences_form.save(commit=False)
            health_conditions = health_conditions_form.save(commit=False)
            weather_preferences.user = request.user
            health_conditions.user = request.user
            weather_preferences.save()
            health_conditions.save()

            request.user.profile.first_login = False
            request.user.profile.save()

            messages.success(request, 'You have successfully registered your weather preferences!')
            return redirect('register_hometown')
        else:
            messages.error(request, 'There was an issue with your form submission. Please correct the errors below.')
    else:
        weather_preferences_form = WeatherPreferencesForm()
        health_conditions_form = HealthConditionsForm()

    context = {
        'weather_preferences_form': weather_preferences_form,
        'health_conditions_form': health_conditions_form,
    }
    return render(request, 'weatherpreferences/base_weather_questions.html', context)

def preference_summary(request):
    weather_preferences = WeatherPreferences.objects.get(user=request.user)
    health_conditions = HealthConditions.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=request.user)

    context = {
        'weather_preferences': weather_preferences,
        'health_conditions': health_conditions,
        'user_profile': user_profile,
    }
    return render(request, 'weatherpreferences/preference_summary.html', context)

from django.utils import timezone
import json
from django.http import JsonResponse
from weatherapi.services import fetch_forecast_by_lat_lon
from .models import WeatherFeedback

from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

import json
from django.http import JsonResponse
from django.utils import timezone


@login_required
@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            print("Raw body:", request.body)  # Log raw request body
            data = json.loads(request.body)
            print("Parsed data:", data)  # Log parsed JSON data

            user = request.user
            # Extract the rating and optional feedback date from the request
            rating = data.get('rating')
            feedback_date = data.get('date')
            user_profile = user.profile
            latitude = user_profile.lat
            longitude = user_profile.lon
            city = user_profile.hometown

            # Debug log for received fields
            print(f"Rating: {rating}, Feedback Date: {feedback_date}")

            if not rating or not feedback_date:
                return JsonResponse({'success': False, 'message': 'Rating or date missing in request.'}, status=400)

            # Fetch the weather data for the user's location
            weather_data = fetch_forecast_by_lat_lon(latitude, longitude, user)
            if not weather_data:
                return JsonResponse({'success': False, 'message': 'Weather data could not be fetched.'}, status=400)

            # Assuming the first entry in weather_data corresponds to today's forecast
            today_weather = weather_data[0]

            # Save or update feedback with weather details
            feedback, created = WeatherFeedback.objects.update_or_create(
                user=user,
                date=feedback_date,
                defaults={
                    'rating': rating,
                    'latitude': latitude,
                    'longitude': longitude,
                    'city': city,
                    'icon': today_weather.get('icon'),
                    'temperature': today_weather.get('temperature'),
                    'temperature_min': today_weather.get('temperature_min'),
                    'temperature_max': today_weather.get('temperature_max'),
                    'wind_speed': today_weather.get('wind_speed'),
                    'wind_dir': today_weather.get('wind_dir'),
                    'wind_angle': today_weather.get('wind_angle'),
                    'cloud_cover': today_weather.get('cloud_cover'),
                    'precipitation_total': today_weather.get('precipitation_total'),
                    'precipitation_type': today_weather.get('precipitation_type'),
                    'stats_temperature_avg': today_weather.get('stats_temperature_avg'),
                    'stats_temperature_avg_min': today_weather.get('stats_temperature_avg_min'),
                    'stats_temperature_avg_max': today_weather.get('stats_temperature_avg_max'),
                    'stats_temperature_record_min': today_weather.get('stats_temperature_record_min'),
                    'stats_temperature_record_max': today_weather.get('stats_temperature_record_max'),
                    'stats_precipitation_avg': today_weather.get('stats_precipitation_avg'),
                    'stats_precipitation_probability': today_weather.get('stats_precipitation_probability'),
                    'stats_wind_avg_speed': today_weather.get('stats_wind_avg_speed'),
                    'stats_wind_avg_angle': today_weather.get('stats_wind_avg_angle'),
                    'stats_wind_avg_dir': today_weather.get('stats_wind_avg_dir'),
                    'stats_wind_max_speed': today_weather.get('stats_wind_max_speed'),
                    'stats_wind_max_gust': today_weather.get('stats_wind_max_gust'),
                }
            )

            return JsonResponse({'success': True, 'message': 'Feedback submitted successfully.'})
        except Exception as e:
            print(f"Error: {e}")  # Log the error
            return JsonResponse({'success': False, 'message': 'An error occurred while processing your request.'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

from django.utils.timezone import now

@login_required
def check_feedback_status(request):
    """Check if the user has submitted feedback for today."""
    if request.method == 'GET':
        today = now().date()
        feedback_exists = WeatherFeedback.objects.filter(user=request.user, date=today).exists()
        return JsonResponse({'has_submitted': feedback_exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def mood_journal(request):
    today = timezone.now().date()

    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            journal_entry = form.save(commit=False)
            journal_entry.user = request.user
            journal_entry.save()
        if 'action_questions' in request.POST:
            return redirect('home')
        return redirect('action_questions')
    else:
        form = JournalEntryForm()


    context = {
        'form': form,
        'today': today,
    }
    return render(request, 'weatherpreferences/mood_journal.html', context)

def action_questions(request):
    today = timezone.now().date()

    if request.method == 'POST':
        form = UserActionsForm(request.POST)
        if form.is_valid():
            user_actions = form.save(commit=False)
            user_actions.user = request.user
            user_actions.save()
            return redirect('home')
    else:
        form = UserActionsForm()

    context = {
        'form': form,
        'today': today,
    }
    return render(request, 'weatherpreferences/action_questions.html', context)


from django.utils.timezone import now
from datetime import timedelta

@login_required
def feedback_chart_data(request):
    date_range = request.GET.get('range', '7d')
    end_date = now().date()
    
    if date_range == '7d':
        start_date = end_date - timedelta(days=7)
    elif date_range == '1m':
        start_date = end_date - timedelta(days=30)
    elif date_range == '6m':
        start_date = end_date - timedelta(days=182)
    elif date_range == '1y':
        start_date = end_date - timedelta(days=365)
    else:
        return JsonResponse({'error': 'Invalid range'}, status=400)

    feedbacks = WeatherFeedback.objects.filter(user=request.user, date__range=[start_date, end_date]).order_by('date')
    data = {
        'dates': [feedback.date.strftime('%Y-%m-%d') for feedback in feedbacks],
        'ratings': [feedback.rating for feedback in feedbacks],
    }
    return JsonResponse(data)
