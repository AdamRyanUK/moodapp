from datetime import date
from django.conf import settings
from .models import DailyForecast, HistoricalForecast
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

def fetch_and_save_forecast(user):
    # Get user's saved geolocation
    user_profile = user.userprofile
    latitude = user_profile.latitude
    longitude = user_profile.longitude

    api_key = "d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici"
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
                    'sunrise': forecast_data['astro']['sun'].get('rise'),
                    'sunset': forecast_data['astro']['sun'].get('set'),
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

def get_forecast_for_location(location):
    api_key = "d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici"
    url = f"https://www.meteosource.com/api/v1/free/point"
    params = {
        'place_id': location,
        'sections': 'daily',
        'timezone': 'UTC',
        'language': 'en',
        'units': 'metric',
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
