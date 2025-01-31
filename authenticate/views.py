import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Profile
from .forms import ChangeProfileForm

def landing_page(request): 
	return render(request, 'authenticate/landing_page.html')

def edit_hometown(request):
    user_profile = request.user.profile
    form = ChangeProfileForm(request.POST or None, instance=user_profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('edit_hometown')
    context = {
        'hometown': user_profile.hometown,
        'latitude': user_profile.lat,
        'longitude': user_profile.lon,
        'form': form,
    }

    return render(request, 'authenticate/edit_hometown.html', context)

def register_hometown(request):
    user_profile = request.user.profile
    form = ChangeProfileForm(request.POST or None, instance=user_profile)

    if request.method == 'POST':
        username = request.POST.get('username')  # Capture the username input

        if form.is_valid():
            user_profile.user.first_name = username  # Save the username to the User model
            user_profile.user.save()
            form.save()
            return redirect('home')
        else:
            return redirect('register_hometown')
            
    context = {
        'hometown': user_profile.hometown,
        'latitude': user_profile.lat,
        'longitude': user_profile.lon,
        'form': form,
    }

    return render(request, 'authenticate/register_hometown.html', context)
