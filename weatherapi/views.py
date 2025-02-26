from datetime import datetime
from venv import logger
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from weatherpreferences.models import WeatherFeedback
from .models import HistoricalForecast
from .services import get_city_suggestions, fetch_hourly_forecast, get_nearest_place
from .moodscore import calculate_mood_score
from django.template.defaultfilters import register
from django.shortcuts import render

def city_autocomplete(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Missing query parameter'}, status=400)
    suggestions = get_city_suggestions(query)
    return JsonResponse({'suggestions': suggestions})

@register.filter
def mood_score_color(mood_score):
    red = 255 - (mood_score * 25)
    green = 255 - ((10 - mood_score) * 25)
    return f'rgb({red},{green},0)'

@login_required
def get_hourly_forecast(request):
    user = request.user
    date = request.GET.get('date')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if not date:
        return JsonResponse({'error': 'No date provided'}, status=400)

    if not latitude or not longitude:
        user_profile = user.userprofile
        latitude = user_profile.latitude
        longitude = user_profile.longitude

    try:
        hourly_data = fetch_hourly_forecast(latitude, longitude, date)

        # Add mood score and icon to each hourly forecast entry
        for hour in hourly_data:
            hour['mood_score'] = calculate_mood_score(request.user, hour)
            hour['mood_score_color'] = mood_score_color(hour['mood_score'])
            hour['icon'] = hour['icon']

        return JsonResponse(hourly_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def nearest_place(request):
    """
    API endpoint to fetch the nearest place based on latitude and longitude.

    Query Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        JsonResponse: A JSON object containing place details or an error message.
    """
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if not lat or not lon:
        return JsonResponse({"error": "Latitude and longitude are required."}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return JsonResponse({"error": "Invalid latitude or longitude values."}, status=400)

    # Fetch nearest place using the service function
    api_key = "d6duuiqm1wlscqmf8e6a4v3y91pugctik2uw9ici" 
    place_data = get_nearest_place(lat, lon, api_key)

    if place_data:
        return JsonResponse(place_data, status=200)
    else:
        return JsonResponse({"error": "Unable to fetch place data. Please try again later."}, status=500)

@login_required
def historical_forecast_view(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        try:
            # Convertir la date sélectionnée en objet date
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            # Chercher tous les HistoricalForecast pour cet user, triés par date_generated
            historical_forecasts = HistoricalForecast.objects.filter(user=request.user).order_by('-date_generated')
            forecast_data = None
            generated_date = None

            # Parcourir les historiques pour trouver un qui contient la date voulue
            for historical in historical_forecasts:
                forecasts = historical.forecasts.filter(date=date_obj)
                if forecasts.exists():
                    forecast_data = [
                        {
                            'day': f.date.strftime('%Y-%m-%d'),
                            'summary': f.summary,
                            'icon': f.icon,
                            'temperature_max': f.temperature_max,
                            'precipitation_total': f.precipitation_total,
                            'wind_speed': f.wind_speed,
                            'cloud_cover': f.cloud_cover,
                        }
                        for f in forecasts
                    ]
                    generated_date = historical.date_generated.strftime('%Y-%m-%d')
                    break  # On sort dès qu’on trouve un match

            context = {
                'selected_date': selected_date,
                'forecast_data': forecast_data,
                'generated_date': generated_date,
                'message': 'Aucune prévision trouvée pour cette date dans l’historique.' if not forecast_data else None
            }
        except ValueError:
            context = {'message': 'Date invalide, utilise le format YYYY-MM-DD, mon pote !'}
    else:
        context = {}

    return render(request, 'weatherapi/historical_forecast.html', context)

@login_required
def weather_feedback_view(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

            # Vérifier que la date de fin n’est pas avant la date de début
            if end_date_obj < start_date_obj:
                return render(request, 'weatherapi/weather_feedback.html', {
                    'message': 'La date de fin doit être après la date de début.'
                })

            # Récupérer les feedbacks dans la plage de dates
            feedbacks = WeatherFeedback.objects.filter(
                user=request.user,
                date__range=(start_date_obj, end_date_obj)
            ).order_by('date')

            if feedbacks.exists():
                feedback_data = [
                    {
                        'day': f.date.strftime('%Y-%m-%d'),
                        'rating': f.rating,
                        'city': f.city,
                        'icon': f.icon,
                        'temperature_max': f.temperature_max,
                        'precipitation_total': f.precipitation_total,
                        'wind_speed': f.wind_speed,
                        'cloud_cover': f.cloud_cover,
                    }
                    for f in feedbacks
                ]
            else:
                feedback_data = None

            context = {
                'start_date': start_date,
                'end_date': end_date,
                'feedback_data': feedback_data,
                'message': 'Aucun feedback trouvé dans cette plage de dates.' if not feedback_data else None
            }
        except ValueError:
            context = {'message': 'Dates invalides, utilise le format YYYY-MM-DD.'}
    else:
        context = {}

    return render(request, 'weatherapi/weather_feedback.html', context)