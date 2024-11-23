
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim # type: ignore
from geopy.exc import GeocoderTimedOut # type: ignore
import requests
from .models import LocationHistory
from django.utils.timezone import now

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