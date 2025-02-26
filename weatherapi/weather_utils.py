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
from weatherpreferences.models import WeatherFeedback

logger = logging.getLogger(__name__)

def calculate_consecutive_days(user, forecast_date, forecast_data, cloud_threshold=75, sunny_threshold=25, rain_threshold=0.1):
    consecutive_cloudy_days = 0
    consecutive_sunny_days = 0
    consecutive_rainy_days = 0
    current_date = date.fromisoformat(forecast_date)

    # Données actuelles
    cloud_cover_current = forecast_data['all_day'].get('cloud_cover', {}).get('total', 0)
    precipitation_current = forecast_data['all_day'].get('precipitation', {}).get('total', 0)

    # Checker les jours précédents dans WeatherFeedback
    prev_date = current_date - timedelta(days=1)
    while prev_date >= current_date - timedelta(days=7):
        prev_feedback = WeatherFeedback.objects.filter(user=user, date=prev_date).first()
        if prev_feedback:
            if prev_feedback.cloud_cover > cloud_threshold:
                consecutive_cloudy_days += 1
            else:
                consecutive_cloudy_days = 0

            if prev_feedback.cloud_cover <= sunny_threshold and prev_feedback.precipitation_total <= rain_threshold:
                consecutive_sunny_days += 1
            else:
                consecutive_sunny_days = 0

            if prev_feedback.precipitation_total > rain_threshold:
                consecutive_rainy_days += 1
            else:
                consecutive_rainy_days = 0
        else:
            break  # Pas de feedback, on s’arrête

        prev_date -= timedelta(days=1)

    # Ajouter le jour actuel
    if cloud_cover_current > cloud_threshold:
        consecutive_cloudy_days += 1
    else:
        consecutive_cloudy_days = 0

    if cloud_cover_current <= sunny_threshold and precipitation_current <= rain_threshold:
        consecutive_sunny_days += 1
    else:
        consecutive_sunny_days = 0

    if precipitation_current > rain_threshold:
        consecutive_rainy_days += 1
    else:
        consecutive_rainy_days = 0

    return {
        'consecutive_cloudy_days': consecutive_cloudy_days,
        'consecutive_sunny_days': consecutive_sunny_days,
        'consecutive_rainy_days': consecutive_rainy_days,
    }

def update_forecast_analysis(forecast):
    """Met à jour ou crée l'analyse associée à une prévision."""
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