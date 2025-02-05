from django.core.exceptions import ObjectDoesNotExist
from weatherpreferences.models import WeatherPreferences

def calculate_mood_score(user, forecast):
    try:
        preferences = WeatherPreferences.objects.get(user=user)
    except ObjectDoesNotExist:
        preferences = None

    mood_score = 10  # Default score

    if preferences:
        # Temperature calculation
        ideal_temp = float(preferences.ideal_temp_max) if preferences.ideal_temp_max else None
        if ideal_temp is not None:
            if isinstance(forecast, dict):
                actual_temp = forecast.get('temperature_max') or forecast.get('temperature')
            else:
                actual_temp = getattr(forecast, 'temperature_max', None) or getattr(forecast, 'temperature', None)

            if actual_temp is not None:
                temp_diff = abs(ideal_temp - actual_temp)
                mood_score -= (temp_diff ** 2) / 30

        # Add your other mood factors here (wind, sun_lover, etc.)

    return max(min(round(mood_score), 10), 1)
