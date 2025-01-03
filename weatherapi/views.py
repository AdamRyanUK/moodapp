from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services import get_city_suggestions, fetch_hourly_forecast
from .moodscore import calculate_mood_score

def city_autocomplete(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'Missing query parameter'}, status=400)
    suggestions = get_city_suggestions(query)
    return JsonResponse({'suggestions': suggestions})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register

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
            hour['mood_score'] = calculate_mood_score(user, hour)
            hour['mood_score_color'] = mood_score_color(hour['mood_score'])
            hour['icon'] = hour['icon']

        return JsonResponse(hourly_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
