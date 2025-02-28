import logging
from datetime import date, timedelta
from .models import DailyForecast, ForecastAnalysis

logger = logging.getLogger(__name__)

def calculate_forecast_differences(forecast_data):
    """Calcule les écarts par rapport aux moyennes historiques pour température max et vent moyen."""
    try:
        # Température maximale
        temp_max_avg = forecast_data['statistics']['temperature'].get('avg_max')
        temp_max_current = forecast_data['all_day'].get('temperature_max')
        temp_max_diff = temp_max_current - temp_max_avg if temp_max_avg is not None and temp_max_current is not None else None

        # Vitesse moyenne du vent
        wind_avg_speed_avg = forecast_data['statistics']['wind'].get('avg_speed')
        wind_avg_speed_current = forecast_data['all_day']['wind'].get('speed')
        wind_avg_speed_diff = wind_avg_speed_current - wind_avg_speed_avg if wind_avg_speed_avg is not None and wind_avg_speed_current is not None else None

        return {
            'temp_max_diff_from_avg': temp_max_diff,
            'wind_ave_speed_diff_from_avg': wind_avg_speed_diff,
        }
    except KeyError as e:
        logger.error(f"Erreur dans les données pour calculer les écarts : {e}")
        return {
            'temp_max_diff_from_avg': None,
            'wind_ave_speed_diff_from_avg': None,
        }

import logging
from datetime import date, timedelta
from weatherpreferences.models import WeatherFeedback, WeatherPreferences

logger = logging.getLogger(__name__)

# weatherapi/weather_utils.py
from weatherpreferences.models import WeatherPreferences

def generate_weather_text(user, weather_data):
    """Generate a personalized weather text based on user preferences and forecast."""
    try:
        prefs = WeatherPreferences.objects.get(user=user)
    except WeatherPreferences.DoesNotExist:
        return "No weather preferences set yet."

    if len(weather_data) < 2:
        return "Not enough forecast data for tomorrow."

    # Demain (weather_data[1])
    tomorrow = weather_data[1]
    temp_max = float(tomorrow['temperature_max']) if tomorrow['temperature_max'] else 0
    cloud_cover = tomorrow['cloud_cover'] if tomorrow['cloud_cover'] else 0
    precipitation = tomorrow['precipitation_total'] if tomorrow['precipitation_total'] else 0
    wind_speed = tomorrow['wind_speed'] if tomorrow['wind_speed'] else 0
    
    logger.debug(f"Tomorrow's data: day={tomorrow['day']}, temp_max={temp_max}, cloud_cover={cloud_cover}, precipitation={precipitation}, wind_speed={wind_speed}")

    # Préférences utilisateur
    ideal_temp_max = float(prefs.ideal_temp_max) if prefs.ideal_temp_max else 25
    ideal_temp_min = float(prefs.ideal_temp_min) if prefs.ideal_temp_min else 15
    sun_lover = prefs.sun_lover
    rain_lover = prefs.rain_lover
    try:
        wind_hater = float(prefs.wind_hater) if prefs.wind_hater else 20
    except (ValueError, TypeError):
        wind_hater = 20

    # Description de demain
    if cloud_cover > 75:
        cloud_text = "cloudy"
    elif cloud_cover < 25:
        cloud_text = "sunny"
    else:
        cloud_text = "partly cloudy"

    # Température avec marge de 3°C
    if temp_max > ideal_temp_max + 3:
        temp_text = "warmer than you like"
    elif temp_max < ideal_temp_min - 3:
        temp_text = "colder than you enjoy"
    elif abs(temp_max - ideal_temp_max) <= 3:
        temp_text = "almost your ideal"
    elif temp_max < ideal_temp_min:
        temp_text = "a bit too cool for you"
    else:
        temp_text = "pretty chilly for your taste"

    rain_text = "with some rain" if precipitation > 0.1 else "with no rain"

    # Évaluation du ressenti pour demain
    score_tomorrow = 0
    reasons = []
    if sun_lover and cloud_cover < 25:
        score_tomorrow += 2  # Gros bonus pour soleil
    elif sun_lover and cloud_cover > 75:
        reasons.append("it’s too cloudy for your sunny vibe")
    if rain_lover and precipitation > 0.1:
        score_tomorrow += 1
    elif not rain_lover and precipitation > 0.1:
        reasons.append("there’s rain you hate")
    if wind_speed < wind_hater:
        score_tomorrow += 1
    elif wind_speed > wind_hater:
        reasons.append("the wind’s too strong")
    if abs(temp_max - ideal_temp_max) <= 3:
        score_tomorrow += 2  # Bonus si proche de l’idéal
    elif ideal_temp_min <= temp_max <= ideal_temp_max:
        score_tomorrow += 1
    else:
        reasons.append("the temp’s off your sweet spot")

    if score_tomorrow >= 4:
        tomorrow_vibe = "which looks awesome for you"
    elif score_tomorrow >= 3:
        tomorrow_vibe = "which should be pretty good"
    elif score_tomorrow >= 2:
        tomorrow_vibe = "which might be okay"
    else:
        tomorrow_vibe = f"and {', and '.join(reasons)} will probably annoy you"

    tomorrow_text = f"Tomorrow will be {cloud_text} with a temperature {temp_text} and {rain_text}, {tomorrow_vibe}."

    # Les 3 prochains jours (jours 2-4)
    next_three = weather_data[2:5]
    if not next_three:
        return tomorrow_text + " No forecast for the next few days."

    avg_cloud = sum(day['cloud_cover'] for day in next_three) / len(next_three)
    avg_precip = sum(day['precipitation_total'] for day in next_three) / len(next_three)
    avg_wind = sum(day['wind_speed'] for day in next_three) / len(next_three)

    if avg_cloud > 75:
        next_cloud = "mostly cloudy"
    elif avg_cloud < 25:
        next_cloud = "mostly sunny"
    else:
        next_cloud = "a mix of sun and clouds"

    score_next = 0
    if sun_lover and avg_cloud < 25:
        score_next += 2
    elif not sun_lover and avg_cloud > 75:
        score_next += 1
    if rain_lover and avg_precip > 0.1:
        score_next += 1
    elif not rain_lover and avg_precip <= 0.1:
        score_next += 1
    if avg_wind < wind_hater:
        score_next += 1

    if score_next >= 4:
        next_vibe = "pretty awesome"
    elif score_next >= 3:
        next_vibe = "pretty good"
    elif score_next >= 2:
        next_vibe = "okay"
    else:
        next_vibe = "not great"

    next_text = f"The next 3 days will be {next_cloud}, so based on your preferences, it’s {next_vibe} for you."

    return f"{tomorrow_text} {next_text}"

def calculate_consecutive_days(user, forecast_date, forecast_data, cloud_threshold=75, sunny_threshold=25, rain_threshold=0.1):
    """Calculate consecutive days based on WeatherFeedback history and current forecast."""
    consecutive_cloudy_days = 0
    consecutive_sunny_days = 0
    consecutive_rainy_days = 0
    current_date = date.fromisoformat(forecast_date)

    # Current day data
    cloud_cover_current = forecast_data['all_day'].get('cloud_cover', {}).get('total', 0)
    precipitation_current = forecast_data['all_day'].get('precipitation', {}).get('total', 0)

    # Start with the current day
    if cloud_cover_current > cloud_threshold:
        consecutive_cloudy_days = 1
    if cloud_cover_current <= sunny_threshold and precipitation_current <= rain_threshold:
        consecutive_sunny_days = 1
    if precipitation_current > rain_threshold:
        consecutive_rainy_days = 1

    # Check previous days in WeatherFeedback
    prev_date = current_date - timedelta(days=1)
    while prev_date >= current_date - timedelta(days=7):  # Limit to 7 days back
        prev_feedback = WeatherFeedback.objects.filter(user=user, date=prev_date).first()
        if prev_feedback:
            # Cloudy streak
            if prev_feedback.cloud_cover > cloud_threshold:
                consecutive_cloudy_days += 1
            else:
                consecutive_cloudy_days = 0  # Break the streak if condition not met

            # Sunny streak
            if prev_feedback.cloud_cover <= sunny_threshold and prev_feedback.precipitation_total <= rain_threshold:
                consecutive_sunny_days += 1
            else:
                consecutive_sunny_days = 0

            # Rainy streak
            if prev_feedback.precipitation_total > rain_threshold:
                consecutive_rainy_days += 1
            else:
                consecutive_rainy_days = 0
        else:
            break  # No feedback, stop looking back

        prev_date -= timedelta(days=1)

    return {
        'consecutive_cloudy_days': consecutive_cloudy_days,
        'consecutive_sunny_days': consecutive_sunny_days,
        'consecutive_rainy_days': consecutive_rainy_days,
    }

def update_forecast_analysis(forecast):
    """Update or create the analysis associated with a forecast."""
    differences = calculate_forecast_differences(forecast.raw_data)
    consecutive_days = calculate_consecutive_days(forecast.user, str(forecast.date), forecast.raw_data)

    ForecastAnalysis.objects.update_or_create(
        forecast=forecast,
        defaults={
            'temp_max_diff_from_avg': differences['temp_max_diff_from_avg'],
            'wind_ave_speed_diff_from_avg': differences['wind_ave_speed_diff_from_avg'],
            'consecutive_cloudy_days': consecutive_days['consecutive_cloudy_days'],
            'consecutive_sunny_days': consecutive_days['consecutive_sunny_days'],
            'consecutive_rainy_days': consecutive_days['consecutive_rainy_days'],
        }
    )