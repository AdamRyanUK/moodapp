
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim # type: ignore
from geopy.exc import GeocoderTimedOut # type: ignore
import requests
from authenticate.models import Location
from django.utils.timezone import now
from datetime import date

def get_nearest_town(latitude, longitude):
    geolocator = Nominatim(user_agent="weather_app")  # Replace with your app's name

    try:
        # Make the API request using Nominatim's reverse geocoding service
        location = geolocator.reverse((latitude, longitude), language='en', exactly_one=True, timeout=10)
        
        # Handle the case when the response is None or geocoding failed
        if location:
            # Now extract the address and see if it contains a town or city
            address_parts = location.raw.get('address', {})
            
            # Check for a valid town or city
            town = address_parts.get('town')
            city = address_parts.get('city')
            
            if town:
                return town
            elif city:
                return city
            else:
                return "Unknown location"

        return "Unable to determine location"
    except GeocoderTimedOut:
        return "Geocoding service timed out. Try again later."

def save_location_history(user, latitude, longitude, city):
    LocationHistory.objects.create(
        user=user,
        latitude=latitude,
        longitude=longitude,
        city=city,
        timestamp=now()  # Set the current time
    )

def get_current_location(profile):
    """
    Determine the current location based on today's date and vacation locations.
    Returns the place name of an active vacation or the profile's hometown.
    """
    today = date.today()
    current_vacation = Location.objects.filter(
        profile=profile,
        location_type='vacation',
        start_date__lte=today,
        end_date__gte=today
    ).first()  # Get first matching vacation if any
    
    if current_vacation:
            return (current_vacation.place_name, current_vacation.lat, current_vacation.lon)
    return (profile.hometown if profile.hometown else "Not set", profile.lat, profile.lon)