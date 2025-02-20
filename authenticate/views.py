import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Profile, Location
from .forms import ChangeProfileForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def landing_page(request): 
	return render(request, 'authenticate/landing_page.html')

@login_required
def edit_hometown(request):
    user_profile = request.user.profile
    form = ChangeProfileForm(request.POST or None, instance=user_profile)

    if request.method == 'POST':
        if form.is_valid():
            old_hometown = user_profile.hometown
            new_hometown = form.cleaned_data['hometown']
            print(f"Old hometown: {old_hometown}, New hometown: {new_hometown}")

            # Removing the condition to always update history
            print("Updating history...")  # Print this to confirm we're always entering this block
            
            # Get the most recent location history entry
            last_history = user_profile.locations.order_by('-start_date').first()
            if last_history:
                last_history.end_date = timezone.now()
                last_history.save()
                print(f"Updated end date for {last_history.place_name} to {last_history.end_date}")
            
            # Create a new history entry for the new hometown
            new_history = Location.objects.create(
                profile=user_profile,
                place_name=new_hometown,
                lat=form.cleaned_data.get('lat', None),
                lon=form.cleaned_data.get('lon', None),
                start_date=timezone.now(),
                location_type= 'hometown'
            )
            print(f"New history entry created: {new_history.place_name}")
            
            # Save the new data to the Profile
            form.save()
            
            return redirect('home')
        else:
            print("Form is not valid")
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
        hometown = request.POST.get('hometown')  # Capture the hometown input
        lat = request.POST.get('lat')  # Capture the latitude input
        lon = request.POST.get('lon')  # Capture the longitude input

        if form.is_valid():
            # Save the username to the User model
            user_profile.user.first_name = username
            user_profile.hometown = hometown
            user_profile.lat = lat
            user_profile.lon = lon
            user_profile.hometown_registered = True

            # Create a new Location entry for hometown we are registering: 
            Location.objects.create(
                profile=user_profile,
                place_name=form.cleaned_data['hometown'],  # Use the new hometown
                lat=form.cleaned_data.get('lat', None),  # Get lat if provided
                lon=form.cleaned_data.get('lon', None),  # Get lon if provided
                start_date=timezone.now(),  # Use the current date and time
                location_type= 'hometown'
            )

            user_profile.user.save()
            form.save()
            return redirect('subscribe')
        else:
            return redirect('register_hometown')
            
    context = {
        'hometown': user_profile.hometown,
        'latitude': user_profile.lat,
        'longitude': user_profile.lon,
        'form': form,
        'block_feedback_script': True,
    }

    return render(request, 'authenticate/register_hometown.html', context)

