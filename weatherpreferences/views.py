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
            request.user.profile.weather_preferences_completed = True

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
            data = json.loads(request.body)
            logger.debug(f"Données reçues : {data}")

            user = request.user
            rating = data.get('rating')
            feedback_date = data.get('date')

            if not rating or not feedback_date:
                return JsonResponse({'success': False, 'message': 'Rating ou date manquant, mec !'}, status=400)

            # Convertir la date
            feedback_date_obj = date.fromisoformat(feedback_date)

            # Récupérer la localisation actuelle depuis Location
            user_profile = user.profile
            today = date.today()
            current_location = user_profile.locations.filter(
                start_date__lte=today,
                end_date__gte=today  # On garde ça même si end_date peut être null
            ).order_by('-start_date').first()

            if not current_location:
                current_location = user_profile.locations.filter(location_type='hometown').first()
                if not current_location:
                    latitude = user_profile.lat
                    longitude = user_profile.lon
                    city = user_profile.hometown
                else:
                    latitude = float(current_location.lat) if current_location.lat else user_profile.lat
                    longitude = float(current_location.lon) if current_location.lon else user_profile.lon
                    city = current_location.place_name
            else:
                latitude = float(current_location.lat) if current_location.lat else user_profile.lat
                longitude = float(current_location.lon) if current_location.lon else user_profile.lon
                city = current_location.place_name

            logger.debug(f"Localisation utilisée : {city} (lat: {latitude}, lon: {longitude})")

            # Fetch les données météo
            weather_data = fetch_forecast_by_lat_lon(latitude, longitude, user)
            if not weather_data:
                return JsonResponse({'success': False, 'message': 'Pas de données météo, ça craint !'}, status=400)

            # Matcher la date du feedback
            today_weather = next(
                (forecast for forecast in weather_data if forecast['day'] == feedback_date),
                weather_data[0]  # Fallback sur le premier jour
            )

            # Sauvegarder le feedback
            feedback, created = WeatherFeedback.objects.update_or_create(
                user=user,
                date=feedback_date_obj,
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

            return JsonResponse({'success': True, 'message': 'Feedback envoyé, t’es un boss !'})
        except Exception as e:
            logger.error(f"Erreur de ouf : {e}")
            return JsonResponse({'success': False, 'message': 'Ça a merdé, désolé mon pote !'}, status=500)
    return JsonResponse({'success': False, 'message': 'Mauvaise méthode, faut du POST, mec !'}, status=400)

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
from datetime import date, timedelta

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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import JournalEntry, WeatherFeedback

@login_required
def display_journal(request):
    # Récupérer le filtre rating depuis la requête GET (s'il existe)
    rating_filter = request.GET.get('rating', None)
    
    # Récupérer les entrées du journal
    journal_entries = JournalEntry.objects.filter(user=request.user).order_by('-date')
    
    # Récupérer les feedbacks météo pour associer les ratings
    feedbacks = WeatherFeedback.objects.filter(user=request.user).values('date', 'rating')
    feedback_dict = {f['date']: f['rating'] for f in feedbacks}
    
    # Ajouter le rating à chaque entrée et filtrer si nécessaire
    filtered_entries = []
    for entry in journal_entries:
        entry.rating = feedback_dict.get(entry.date, None)
        if rating_filter:  # Si un filtre est appliqué
            if entry.rating == int(rating_filter):  # Filtrer par rating
                filtered_entries.append(entry)
        else:
            filtered_entries.append(entry)  # Pas de filtre, tout inclure
    
    return render(request, 'weatherpreferences/display_journal.html', {
        'journal_entries': filtered_entries,
        'current_rating': rating_filter  # Pour garder la sélection dans le dropdown
    })