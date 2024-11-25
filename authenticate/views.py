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

@login_required
def home(request):
    # Initialize city and weather data as None
    city = None
    weather_data = None

    # Get the latitude and longitude from the user's profile
    user_profile = request.user.userprofile
    latitude = user_profile.latitude if user_profile.latitude else None
    longitude = user_profile.longitude if user_profile.longitude else None

    # Check if latitude and longitude are available
    if latitude and longitude:
        city = get_nearest_town(latitude, longitude)  # Call the geocoding function

        # Fetch the latest weather forecast for the user
        latest_forecast = DailyForecast.objects.filter(user=request.user).order_by('-date')[:7]

        weather_data = []
        if latest_forecast.exists():
            for forecast in latest_forecast:
                weather_data.append({
                    'day': forecast.date,
                    'summary': forecast.summary,
                    'temperature': forecast.temperature,
                    'temperature_min': forecast.temperature_min,
                    'temperature_max': forecast.temperature_max,
                    'precipitation_amt': forecast.precipitation_total,
                    'precipitation_type': forecast.precipitation_type,
                    'wind_speed': forecast.wind_speed,
                })
        else:
            weather_data = []

    # Check if location saved
    location_saved = request.session.get('location_saved', False)  # Default to False if not set

    # Log the weather_data to verify it's being passed correctly
    print(weather_data)
    
    # Pass the latitude, longitude, city, and weather data to the template
    return render(request, 'authenticate/home.html', {
        'latitude': latitude,
        'longitude': longitude,
        'city': city,
        'weather_data': weather_data,
        'location_saved': location_saved,
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
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('You Have Registered...'))
			return redirect('home')
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