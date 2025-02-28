# core/moodscore.py
import logging
from django.core.exceptions import ObjectDoesNotExist
from weatherpreferences.models import WeatherPreferences
from weatherapi.weather_utils import calculate_consecutive_days

logger = logging.getLogger(__name__)

def calculate_mood_score(user, forecast):
    """Calculate mood score based on weather preferences and consecutive days."""
    try:
        preferences = WeatherPreferences.objects.get(user=user)
    except ObjectDoesNotExist:
        preferences = None

    mood_score = 5  # Base neutre

    if preferences:
        # Préférences
        ideal_temp_max = float(preferences.ideal_temp_max) if preferences.ideal_temp_max else 25
        ideal_temp_min = float(preferences.ideal_temp_min) if preferences.ideal_temp_min else 15
        sun_lover = preferences.sun_lover
        rain_lover = preferences.rain_lover
        try:
            wind_hater = float(preferences.wind_hater) if preferences.wind_hater else 20
        except (ValueError, TypeError):
            wind_hater = 20  # Fallback si 'true' ou autre merde

        # Données du jour
        if isinstance(forecast, dict):
            temp_max = float(forecast.get('temperature_max', forecast.get('temperature', 0)))
            cloud_cover = forecast.get('cloud_cover', 0)
            precipitation = forecast.get('precipitation_total', 0)
            wind_speed = forecast.get('wind_speed', 0)
            forecast_date = forecast['day']
        else:
            temp_max = getattr(forecast, 'temperature_max', getattr(forecast, 'temperature', 0))
            cloud_cover = getattr(forecast, 'cloud_cover', 0)
            precipitation = getattr(forecast, 'precipitation_total', 0)
            wind_speed = getattr(forecast, 'wind_speed', 0)
            forecast_date = str(forecast.date)

        # Temp impact
        temp_diff = abs(ideal_temp_max - temp_max)
        if temp_diff <= 3:
            mood_score += 2  # Presque idéal
        elif ideal_temp_min <= temp_max <= ideal_temp_max:
            mood_score += 1  # Dans la plage
        else:
            mood_score -= int(temp_diff / 3)  # Pénalité progressive

        # Calcul des jours consécutifs
        consecutive = calculate_consecutive_days(
            user, 
            forecast_date, 
            {'all_day': {'cloud_cover': {'total': cloud_cover}, 'precipitation': {'total': precipitation}}}
        )
        cloudy_streak = consecutive['consecutive_cloudy_days']
        sunny_streak = consecutive['consecutive_sunny_days']
        rainy_streak = consecutive['consecutive_rainy_days']

        # Soleil pour sun_lover
        if sun_lover:
            if cloud_cover < 25:  # Jour ensoleillé
                if cloudy_streak > 1 and sunny_streak == 1:  # 1er jour soleil après nuages
                    mood_score += 4  # Gros boost lapin
                    logger.debug(f"Sun lover boost: First sunny day after {cloudy_streak} cloudy days")
                elif sunny_streak <= 3:
                    mood_score += 2  # Soleil frais
                else:
                    mood_score += 1  # Soleil routinier
            elif cloud_cover > 75:  # Nuageux
                if cloudy_streak == 1:
                    mood_score -= 1  # 1er jour OK
                elif cloudy_streak <= 3:
                    mood_score -= 2  # Ça commence à gaver
                else:
                    mood_score -= 3  # Trop de nuages, il craque

        # Pluie
        if rain_lover:
            if precipitation > 0.1:
                if rainy_streak == 1:
                    mood_score += 2  # Première pluie = cool
                else:
                    mood_score += 1  # Pluie sympa
            else:
                mood_score -= 1  # Pas de pluie, bof
        else:
            if precipitation > 0.1:
                if rainy_streak == 1:
                    mood_score -= 2  # Première pluie = chiant
                elif rainy_streak <= 3:
                    mood_score -= 3  # Plus de pluie = pire
                else:
                    mood_score -= 4  # Trop de pluie = KO
            else:
                mood_score += 1  # Pas de pluie = bien

        # Vent
        if wind_speed > wind_hater:
            mood_score -= 2
        else:
            mood_score += 1

    # Limiter entre 1 et 10
    mood_score = max(1, min(10, round(mood_score)))
    logger.debug(f"Mood score for {forecast_date}: {mood_score}, streaks: cloudy={cloudy_streak}, sunny={sunny_streak}, rainy={rainy_streak}")
    return mood_score