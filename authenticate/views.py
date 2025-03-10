import json
from venv import logger
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from django.utils.translation import activate

from .models import Profile, Location
from .forms import ChangeProfileForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from core.utils import get_current_location
from weatherapi.services import get_nearest_place

def landing_page(request): 
    activate('fr')  # Bien aligné avec 4 espaces
    return render(request, 'authenticate/landing_page.html')  # Cette ligne aussi


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
            
            # Mettre à jour current_location avec le nouveau hometown
            user_profile.current_location = new_hometown
            form.save() # Save the new data to the Profile
            user_profile.save()  # Sauvegarde current_location
            
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
        username = request.POST.get('username')
        hometown = request.POST.get('hometown')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')

        logger.info(f"Données reçues : username={username}, hometown={hometown}, lat={lat}, lon={lon}")

        if form.is_valid():
            # Sauvegarde des données de base
            user_profile.user.first_name = username
            user_profile.hometown = hometown
            user_profile.lat = lat
            user_profile.lon = lon
            user_profile.hometown_registered = True
            user_profile.current_location = hometown

            # Appel à Meteosource pour les données de localisation
            api_key = "d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici"  
            place_data = get_nearest_place(lat, lon, api_key)

            logger.info(f"Réponse de get_nearest_place : {place_data}")

            if place_data:
                # Récupérer le nom du pays (au lieu du code)
                country = place_data.get('country', '').lower()  # Convertir en minuscules pour éviter les problèmes de casse
                logger.info(f"Pays trouvé : {country}")

                # Mapper le nom du pays aux unités
                unit_mapping = {
                    'united states of america': 'us',  # États-Unis
                    'united kingdom': 'uk',            # Royaume-Uni
                    'canada': 'ca',                    # Canada
                    # Par défaut : métrique pour tous les autres pays
                }
                user_profile.units = unit_mapping.get(country, 'metric')
                logger.info(f"Unités assignées : {user_profile.units}")
            else:
                # Défaut si l’appel échoue
                user_profile.units = 'metric'
                logger.warning("Échec de récupération des données de localisation, utilisation de 'metric'.")

            # Créer une nouvelle entrée Location
            Location.objects.create(
                profile=user_profile,
                place_name=form.cleaned_data['hometown'],
                lat=form.cleaned_data.get('lat', None),
                lon=form.cleaned_data.get('lon', None),
                start_date=timezone.now(),
                location_type='hometown'
            )

            # Sauvegarder les modifications
            user_profile.user.save()
            user_profile.save()
            logger.info(f"Profil sauvegardé avec units={user_profile.units}")

            return redirect('subscribe')
        else:
            logger.error("Formulaire invalide")
            return redirect('register_hometown')

    context = {
        'hometown': user_profile.hometown,
        'latitude': user_profile.lat,
        'longitude': user_profile.lon,
        'form': form,
        'block_feedback_script': True,
    }

    return render(request, 'authenticate/register_hometown.html', context)