from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .models import CitySearch 
from weatherapi.models import DailyForecast
from weatherapi.services import fetch_forecast_by_lat_lon, fetch_and_save_forecast
from weatherapi.moodscore import calculate_mood_score
from datetime import date as datetime_date
from datetime import datetime
from weatherpreferences.models import WeatherFeedback
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from core.feedbackanomaly.anomaly_calculations import fetch_anomaly_data
from authenticate.models import Location, Profile
from django.http import HttpResponseForbidden
from .utils import get_current_location  # Import from utils.py

def serialize_weather_data(weather_data):
    """Convert datetime and timedelta objects in weather_data to strings."""
    for forecast in weather_data:
        for key, value in forecast.items():
            if isinstance(value, datetime):
                forecast[key] = value.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
            elif isinstance(value, timedelta):
                forecast[key] = str(value)  # Convert timedelta to string (e.g., '1 day, 2:30:00')
    return weather_data

def home(request):
    if request.user.is_authenticated:
        city = None
        city_first_part = None
        weather_data = None
        location = request.GET.get('location')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        # Fetch the user profile once
        user_profile = request.user.profile

        if location and latitude and longitude:
            # Fetch forecast for the entered location using lat/lon
            weather_data = fetch_forecast_by_lat_lon(latitude, longitude, request.user)

            # Add mood score to the weather data for searchable forecasts
            for forecast in weather_data:
                forecast['mood_score'] = calculate_mood_score(request.user, forecast)

            # Ensure the 'day' attribute is a datetime object
            for forecast in weather_data:
                if isinstance(forecast['day'], str):
                    forecast['day'] = datetime.strptime(forecast['day'], '%Y-%m-%d')

                forecast['day'] = forecast['day'].strftime('%Y-%m-%d')
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
            # Si aucune localisation n’est fournie via GET, on détermine la localisation actuelle
            city, lat, lon = get_current_location(user_profile)
            latitude = lat
            longitude = lon  # Récupère le nom de la localisation actuelle

            if latitude and longitude:
                fetch_and_save_forecast(request.user, latitude=latitude, longitude=longitude)
                latest_forecast = DailyForecast.objects.filter(user=request.user).order_by('date')[:7]

                weather_data = [
                    {
                        'day': forecast.date.strftime('%Y-%m-%d'),
                        'summary': forecast.summary,
                        'icon': forecast.icon,
                        'temperature_min': forecast.temperature_min,
                        'temperature_max': forecast.temperature_max,
                        'precipitation_total': forecast.precipitation_total,
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
                city_first_part = city

        # Extract sunrise and sunset for the first day
        first_day_sunrise = weather_data[0]['sunrise'] if weather_data else None
        first_day_sunset = weather_data[0]['sunset'] if weather_data else None
        first_day_length = weather_data[0]['day_length'] if weather_data else None

        # Query the most selected cities by the current user
        most_selected_cities = CitySearch.objects.filter(user=request.user).order_by('-search_count')[:10]

        # Add city_first_part to most_selected_cities for easy template rendering
        for city_search in most_selected_cities:
            city_search.city_first_part = city_search.city.split(',')[0] if ',' in city_search.city else city_search.city

        # Store weather data in session
        if weather_data:
            request.session['weather_data'] = serialize_weather_data(weather_data)

        return render(request, 'home.html', {
            'city_first_part': city_first_part,
            'city': city,
            'weather_data': weather_data,
            'first_day_sunrise': first_day_sunrise,
            'first_day_sunset': first_day_sunset,
            'first_day_length': first_day_length,
            'most_selected_cities': most_selected_cities,
            'latitude': latitude, 
            'longitude': longitude
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
    return render(request, 'insights.html')

def mood_forecast_graph(request):
    if request.user.is_authenticated:
        # Retrieve the weather data from the session
        weather_data = request.session.get('weather_data')

        if not weather_data:
            # Handle the case where there is no weather data (perhaps redirect to home or show an error)
            return redirect('home')

        return render(request, 'mood_forecast_graph.html', {
            'weather_data': weather_data,  # Use the weather data here
        })
    else:
        return render(request, 'authenticate/landing_page.html')

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
    return render(request, 'calendar.html', context)

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

def csrf_failure_view(request, reason=""):
    return render(request, "csrf_failure.html", {"message": "Please refresh the page and try again."}, status=403)

@login_required
def location_display(request):
    if request.method == 'POST' and 'remove_id' in request.POST:
        location_id = request.POST.get('remove_id')
        try:
            location = Location.objects.get(id=location_id, profile=request.user.profile)
            location.delete()
            return HttpResponseRedirect(reverse('locations'))  # Redirect back to the same page after deletion
        except Location.DoesNotExist:
            pass  # Optionally add error handling here, e.g., messages.error(request, "Location not found")
    
    user_locations = Location.objects.filter(profile=request.user.profile).order_by('-start_date')
    current_location = get_current_location(request.user.profile)  # Call the function from utils.py
    
    context = {
        'locations': user_locations,
        'hometown': request.user.profile.hometown,
        'current_location': current_location,
    }
    
    return render(request, 'locations.html', context)

@login_required
def vacation_submit(request):
    if request.method == 'POST':
        print('POST request received')
        print('POST Data:', request.POST)
        
        place_name = request.POST.get('vacationLocation')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        start_date = request.POST.get('vacationStartDate')
        end_date = request.POST.get('vacationEndDate')
        
        print('Received Values:')
        print('Vacation Location:', place_name)
        print('Vacation Start Date:', start_date)
        print('Vacation End Date:', end_date)
        print('Latitude:', lat)
        print('Longitude:', lon)
        
        # Convert dates to datetime objects if they're not already
        try:
            # Validate dates - this assumes they're in YYYY-MM-DD format
            new_start = start_date  # You might need to convert with datetime.strptime if from a different format
            new_end = end_date if end_date else None  # Handle case where end_date is optional
            
            # Check for existing overlapping vacations
            overlapping = Location.objects.filter(
                profile=request.user.profile,
                location_type='vacation'
            ).filter(
                Q(start_date__lte=new_end if new_end else new_start) &
                Q(end_date__gte=new_start) if new_end else 
                Q(start_date__lte=new_start)
            ).exists()
            
            if overlapping:
                locations_url = reverse('locations')  # Generate the URL in Python
                messages.error(
                    request, 
                    f'You already have a vacation entered for these dates. '
                    f'Please <a href="{locations_url}">edit your locations</a> instead.',
                    extra_tags='safe'  # Add this tag to indicate HTML is safe
                )
                return redirect('vacation')  # Redirect back to vacation submission page
                
            # If no overlap, create the new location
            Location.objects.create(
                profile=request.user.profile,
                place_name=place_name,
                lat=lat,
                lon=lon,
                start_date=start_date,
                end_date=end_date,
                location_type='vacation'
            )
            print("Location saved successfully")
            messages.success(request, 'Vacation location added successfully!')
            return redirect('locations')
            
        except ValueError as e:
            print(f"Date format error: {e}")
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
        except Exception as e:
            print(f"Error saving location: {e}")
            messages.error(request, 'An error occurred while saving your location.')
        
        return redirect('vacation')  # Redirect back if there's an error
        
    return render(request, 'vacation.html')