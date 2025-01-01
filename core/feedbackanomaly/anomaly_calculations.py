from datetime import timedelta
from django.utils import timezone
from weatherpreferences.models import WeatherFeedback

def fetch_anomaly_data(user, start_date, end_date):
    feedbacks = WeatherFeedback.objects.filter(user=user, date__range=(start_date, end_date)).order_by('date')

    dates = []
    temperature_anomalies = []
    wind_anomalies = []
    precipitation_anomalies = []
    ratings = []

    for feedback in feedbacks:
        if feedback.stats_temperature_avg is not None:
            dates.append(feedback.date)
            ratings.append(feedback.rating)
            
            temperature_anomalies.append(feedback.temperature - feedback.stats_temperature_avg)
            wind_anomalies.append(feedback.wind_speed - feedback.stats_wind_avg_speed)
            precipitation_anomalies.append(feedback.precipitation_total - feedback.stats_precipitation_avg)

    return {
        'dates': dates,
        'ratings': ratings,
        'temperature_anomalies': temperature_anomalies,
        'wind_anomalies': wind_anomalies,
        'precipitation_anomalies': precipitation_anomalies,
    }
