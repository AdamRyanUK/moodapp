import json
from django.http import JsonResponse
from datetime import date
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authenticate.models import UserProfile
from .models import WeatherFeedback, HealthConditions, WeatherPreferences
from authenticate.models import UserProfile
from .forms import WeatherPreferencesForm, HealthConditionsForm
from weatherapi.services import fetch_forecast_by_lat_lon

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
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
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

@login_required
def feedback_calendar_view(request):
    feedbacks = WeatherFeedback.objects.filter(user=request.user).order_by('date')
    return render(request, 'weatherpreferences/my_history.html', {'feedbacks': feedbacks})

    def get(self, request):
        context = {
            'is_authenticated': request.user.is_authenticated,
        }
        return render(request, 'your_template.html', context)

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
            messages.success(request, ('You Have Registered Your Weather Preferences...'))
            return redirect('preference-summary')
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
    user_profile = UserProfile.objects.get(user=request.user)

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

@csrf_exempt
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract the data from the request
        rating = data.get('rating')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        city = data.get('city')

        # Fetch the weather data for the user's location
        weather_data = fetch_forecast_by_lat_lon(latitude, longitude)

        # If weather data is available, save the forecast variables along with the feedback
        if weather_data:
            # Assuming the first entry in weather_data is today's forecast
            today_weather = weather_data[0]
            
            # Create or update the feedback record with the forecast data
            feedback, created = WeatherFeedback.objects.update_or_create(
                user=request.user,
                date=timezone.now().date(),
                defaults={
                    'rating': rating,
                    'latitude': latitude,
                    'longitude': longitude,
                    'city': city,
                    'icon': today_weather.get('icon'),
                    'temperature': today_weather.get('temperature_min'),
                    'temperature_min': today_weather.get('temperature_min'),
                    'temperature_max': today_weather.get('temperature_max'),
                    'wind_speed': today_weather.get('wind_speed'),
                    'precipitation_total': today_weather.get('precipitation_amt'),
                    'precipitation_type': today_weather.get('precipitation_type'),
                }
            )
            
            return JsonResponse({'success': True, 'message': 'Your feedback and weather data have been saved.'})
        else:
            return JsonResponse({'success': False, 'message': 'Weather data could not be fetched.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

from django.utils.timezone import now

@login_required
def check_feedback_status(request):
    """Check if the user has submitted feedback for today."""
    if request.method == 'GET':
        today = now().date()
        feedback_exists = WeatherFeedback.objects.filter(user=request.user, date=today).exists()
        return JsonResponse({'has_submitted': feedback_exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
