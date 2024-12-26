from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages 
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm, EditProfileForm
from django.shortcuts import render
from .models import UserProfile


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
            # Save the user from the form
            user = form.save()

            # Extract data from the POST request
            hometown = request.POST.get('hometown', '')
            latitude = request.POST.get('latitude', None)
            longitude = request.POST.get('longitude', None)
            country = request.POST.get('country', None)

            # Determine the units based on the country
            if country == 'United States of America':
                units = 'us'
            elif country == 'United Kingdom':
                units = 'uk'
            elif country == 'Canada':
                units = 'ca'
            else:
                units = 'metric'  # Default for all other countries
            
            # Create or update the UserProfile
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'hometown': hometown, 'latitude': latitude, 'longitude': longitude, 'units': units}
            )
            if not created:
                user_profile.hometown = hometown
                user_profile.latitude = latitude
                user_profile.longitude = longitude
                user_profile.units = units
                user_profile.save()

            # Authenticate and log the user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            # Display a success message and redirect to the next step
            messages.success(request, 'You have registered successfully!')
            return redirect('register_weather_preferences')
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

def landing_page(request): 
	return render(request, 'authenticate/landing_page.html')


