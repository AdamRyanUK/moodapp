from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import UserProfile, LocationHistory
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from weatherapi.models import DailyForecast
from .utils import get_nearest_town  # Import the reverse geocoding function
from datetime import date
from weatherapi.models import DailyForecast, WeatherFeedback
from weatherapi.services import fetch_and_save_forecast, get_forecast_for_location
from django.db import transaction
from django.db import IntegrityError


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

    return render(request, 'authenticate/home.html', {
        'city': city,
        'weather_data': weather_data,
    })

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You Have Been Logged In!'))
			return redirect('home')

		else:
			messages.success(request, ('Error Logging In - Please Try Again...'))
			return redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ('You Have Been Logged Out...'))
	return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user

            # Now create or update the UserProfile with additional information (like preferred temperature)
            preferred_temperature_min = form.cleaned_data.get('preferred_temperature_min')
            preferred_temperature_max = form.cleaned_data.get('preferred_temperature_max')

            # Get or update the UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # If profile already exists, we update it
            user_profile.preferred_temperature_min = preferred_temperature_min
            user_profile.preferred_temperature_max = preferred_temperature_max
            user_profile.save()

            # Handle latitude and longitude if needed
            # If you want to set the lat/lon from geolocation, you can do it here

            messages.success(request, 'Your account has been created! Please log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)



def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You Have Edited Your Profile...'))
			return redirect('home')
	else:
		form = EditProfileForm(instance=request.user)
	
	context = {'form': form}
	return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You Have Edited Your Password...'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)
	
	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)

# Ensure the user is logged in before updating location
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
    
    return render(request, 'authenticate/location_history.html', {
        'history': history,
    })

@login_required
def feedback_calendar_view(request):
    feedbacks = WeatherFeedback.objects.filter(user=request.user).order_by('date')
    return render(request, 'authenticate/my_history.html', {'feedbacks': feedbacks})

@login_required
def insights(request):
    # Get the user's feedback data
    feedbacks = WeatherFeedback.objects.filter(user=request.user).order_by('date')
    
    # Calculate the average rating
    total_ratings = 0
    for feedback in feedbacks:
        total_ratings += feedback.rating
    average_rating = total_ratings / len(feedbacks) if feedbacks else 0
    
    return render(request, 'authenticate/insights.html', {
        'feedbacks': feedbacks,
        'average_rating': average_rating,
    })