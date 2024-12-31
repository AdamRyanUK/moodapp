from datetime import date
from django.conf import settings
from .models import DailyForecast, HistoricalForecast
import requests
import logging
import pycountry
import requests
from datetime import datetime
from django.utils.dateparse import parse_datetime

# Set up logging
logger = logging.getLogger(__name__)

# my API key
api_key = "d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici" 

def fetch_and_save_forecast(user):
    # Get user's saved geolocation
    user_profile = user.userprofile
    latitude = user_profile.latitude
    longitude = user_profile.longitude

    url = f"https://www.meteosource.com/api/v1/startup/point"
    params = {
        'lat': latitude,
        'lon': longitude,
        'sections': 'daily',
        'language': 'en',
        'units': 'auto',  
        'key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
        logger.debug(f"Received data: {data}")

        # Fetch current forecasts for the user
        current_forecasts = DailyForecast.objects.filter(user=user)
        
        # Create a historical forecast record with current forecasts
        if current_forecasts.exists():
            historical_forecast = HistoricalForecast.objects.create(user=user)
            historical_forecast.forecasts.set(current_forecasts)
            historical_forecast.save()

        # Remove old forecasts
        DailyForecast.objects.filter(user=user, date__lt=date.today()).delete()

        # Loop through the daily forecast data (e.g., the next 7 days)
        for forecast_data in data['daily']['data']:
            logger.debug(f"Processing forecast for date: {forecast_data['day']}")
            # Update or create DailyForecast entry for the user
            
            sunrise_str = forecast_data['astro']['sun'].get('rise')
            sunset_str = forecast_data['astro']['sun'].get('set')

            sunrise = datetime.fromisoformat(sunrise_str)
            sunset = datetime.fromisoformat(sunset_str)

                # Calculate day length
            day_length = sunset - sunrise

            DailyForecast.objects.update_or_create(
                user=user,
                date=forecast_data['day'],
                defaults={
                    'summary': forecast_data.get('summary'),
                    'weather': forecast_data['all_day'].get('weather'),
                    'icon': forecast_data['all_day'].get('icon'),
                    'temperature': forecast_data['all_day'].get('temperature'),
                    'temperature_min': forecast_data['all_day'].get('temperature_min'),
                    'temperature_max': forecast_data['all_day'].get('temperature_max'),
                    'wind_speed': forecast_data['all_day']['wind'].get('speed'),
                    'wind_dir': forecast_data['all_day']['wind'].get('dir'),
                    'wind_angle': forecast_data['all_day']['wind'].get('angle'),
                    'cloud_cover': forecast_data['all_day'].get('cloud_cover', {}).get('total', 0),
                    'precipitation_total': forecast_data['all_day'].get('precipitation', {}).get('total', 0),
                    'precipitation_type': forecast_data['all_day'].get('precipitation', {}).get('type', ''),
                    'sunrise': sunrise,
                    'sunset': sunset,
                    'day_length': day_length,
                    'moon_phase': forecast_data['astro']['moon'].get('phase'),
                    'moonrise': forecast_data['astro']['moon'].get('rise'),
                    'moonset': forecast_data['astro']['moon'].get('set'),
                    'stats_temperature_avg': forecast_data['statistics']['temperature'].get('avg'),
                    'stats_temperature_avg_min': forecast_data['statistics']['temperature'].get('avg_min'),
                    'stats_temperature_avg_max': forecast_data['statistics']['temperature'].get('avg_max'),
                    'stats_temperature_record_min': forecast_data['statistics']['temperature'].get('record_min'),
                    'stats_temperature_record_max': forecast_data['statistics']['temperature'].get('record_max'),
                    'stats_precipitation_avg': forecast_data['statistics']['precipitation'].get('avg'),
                    'stats_precipitation_probability': forecast_data['statistics']['precipitation'].get('probability'),
                    'stats_wind_avg_speed': forecast_data['statistics']['wind'].get('avg_speed'),
                    'stats_wind_avg_angle': forecast_data['statistics']['wind'].get('avg_angle'),
                    'stats_wind_avg_dir': forecast_data['statistics']['wind'].get('avg_dir'),
                    'stats_wind_max_speed': forecast_data['statistics']['wind'].get('max_speed'),
                    'stats_wind_max_gust': forecast_data['statistics']['wind'].get('max_gust'),
                    'raw_data': forecast_data  # Save raw data for debugging/future
                }
            )
            logger.debug(f"Saved forecast for date: {forecast_data['day']}")

        return data['daily']['data']  # Return the entire forecast data

    except requests.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
        raise

    except KeyError as e:
        logger.error(f"Missing expected data in weather response: {e}")
        raise

def get_forecast_for_location(user, location):

    url = f"https://www.meteosource.com/api/v1/free/point"
    params = {
        'place_id': location,
        'sections': 'daily',
        'timezone': 'UTC',
        'language': 'en',
        'units': 'auto',
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        weather_data = []
        for forecast_data in data['daily']['data']:
            weather_data.append({
                'day': forecast_data['day'],
                'summary': forecast_data.get('summary'),
                'temperature': forecast_data['all_day'].get('temperature'),
                'temperature_min': forecast_data['all_day'].get('temperature_min'),
                'temperature_max': forecast_data['all_day'].get('temperature_max'),
                'precipitation_amt': forecast_data['all_day'].get('precipitation', {}).get('total'),
                'precipitation_type': forecast_data['all_day'].get('precipitation', {}).get('type'),
                'wind_speed': forecast_data['all_day'].get('wind', {}).get('speed'),
                'sunrise': forecast_data['astro']['sun'].get('rise'),
                'sunset': forecast_data['astro']['sun'].get('set'),
                'icon': forecast_data['all_day'].get('icon'),
            })

        return weather_data, location  # Return weather data and the location (city name)
    except requests.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
        return [], "Unknown"
    except KeyError as e:
        logger.error(f"Missing expected data in weather response: {e}")
        return [], "Unknown"

    return [], "Unknown"

def get_country_code(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2.lower()
    except LookupError:
        return None

def get_city_suggestions(query):
    url = f"https://www.meteosource.com/api/v1/startup/find_places_prefix?text={query}&language=en&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        suggestions = []
        unique_place_ids = set()
        for city in data:  # Directly iterate through the list
            if city['place_id'] not in unique_place_ids:
                unique_place_ids.add(city['place_id'])
                country_code = get_country_code(city['country'])
                suggestions.append({
                    'place_id': city['place_id'],
                    'name': city['name'],
                    'adm_area1': city.get('adm_area1', ''),
                    'country': city['country'],
                    'country_code': country_code,
                    'lat': city.get('lat', ''),
                    'lon': city.get('lon', '')
                })
        return suggestions
    return []

import requests
import logging

def parse_coordinate(coord):
    value = float(coord[:-1])
    if coord[-1] in ['S', 'W']:
        return -value
    return value

def fetch_forecast_by_lat_lon(lat, lon, user):
    api_key = "d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici"
    url = f"https://www.meteosource.com/api/v1/startup/point"

    user_profile = user.userprofile
    unit_system = user_profile.units
    
    # Set the unit system to the user's preference
    params = {
        'lat': lat,
        'lon': lon,
        'sections': 'daily',
        'language': 'en',
        'units': unit_system,  # Use the unit system from user's profile
        'key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()  # Parse the JSON response

        # Check if the expected data structure exists
        if 'daily' in data and 'data' in data['daily']:
            weather_data = []
            for forecast_data in data['daily']['data']:
                # Parse sunrise and sunset times
                sunrise_str = forecast_data['astro']['sun'].get('rise')
                sunset_str = forecast_data['astro']['sun'].get('set')

                sunrise = datetime.fromisoformat(sunrise_str)
                sunset = datetime.fromisoformat(sunset_str)

                # Calculate day length
                day_length = sunset - sunrise

                # Extract relevant weather data
                weather_data.append({
                    'day': forecast_data.get('day'),
                    'summary': forecast_data.get('summary'),
                    'icon': forecast_data['all_day'].get('icon'),
                    'temperature': forecast_data['all_day'].get('temperature'),
                    'temperature_min': forecast_data['all_day'].get('temperature_min'),
                    'temperature_max': forecast_data['all_day'].get('temperature_max'),
                    'precipitation_amt': forecast_data['all_day'].get('precipitation', {}).get('total', 0),
                    'precipitation_type': forecast_data['all_day'].get('precipitation', {}).get('type', ''),
                    'precipitation_total': forecast_data['all_day'].get('precipitation', {}).get('total', 0),
                    'sunrise': sunrise,
                    'sunset': sunset,
                    'day_length': day_length,
                    'wind_speed': forecast_data['all_day']['wind'].get('speed'),
                })
            return weather_data
        else:
            logger.error("API response does not contain expected 'daily' or 'data' fields.")
            return []

    except requests.RequestException as e:
        logger.error(f"Failed to fetch weather data: {e}")
        return []
    except KeyError as e:
        logger.error(f"Missing expected data in response: {e}")
        return []
