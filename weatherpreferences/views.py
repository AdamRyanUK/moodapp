import json
from django.http import JsonResponse
from datetime import date
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authenticate.models import UserProfile
from .models import LocationHistory, WeatherFeedback, HealthConditions, WeatherPreferences
from authenticate.models import UserProfile
from .forms import WeatherPreferencesForm, HealthConditionsForm

@csrf_exempt  # Add this to bypass CSRF for API calls (be mindful of CSRF security in production)
@login_required
def update_location(request):
    if request.method == 'POST':
        # Parse the latitude and longitude from the incoming request
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            # Save the location to the user's profile
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.latitude = latitude
            user_profile.longitude = longitude
            user_profile.save()

            return JsonResponse({'status': 'success', 'message': 'Location updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def location_history(request):

    # Get the user's location history
    history = LocationHistory.objects.filter(user=request.user).order_by('-timestamp')
    
    return render(request, 'userpreferences/location_history.html', {
        'history': history,
    })

@login_required
def feedback_calendar_view(request):
    feedbacks = WeatherFeedback.objects.filter(user=request.user).order_by('date')
    return render(request, 'userpreferences/my_history.html', {'feedbacks': feedbacks})

@method_decorator(csrf_exempt, name='dispatch')
class SubmitFeedbackView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        try:
            rating = int(request.POST.get('rating'))
            if rating not in range(1, 6):
                return JsonResponse({'error': 'Invalid rating'}, status=400)

            today = date.today()

            feedback, created = WeatherFeedback.objects.update_or_create(
                user=request.user,
                date=today,
                defaults={'rating': rating}
            )
            return JsonResponse({'success': True, 'created': created})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def register_weather_preferences(request):
    if request.method == 'POST':
        weather_preferences_form = WeatherPreferencesForm(request.POST)
        health_conditions_form = HealthConditionsForm(request.POST)
        if weather_preferences_form.is_valid() and health_conditions_form.is_valid():
            weather_preferences = weather_preferences_form.save(commit=False)
            health_conditions = health_conditions_form.save(commit=False)
            weather_preferences.user = request.user
            health_conditions.user = request.user
            weather_preferences.save()
            health_conditions.save()
            messages.success(request, ('You Have Registered Your Weather Preferences...'))
            return redirect('preference-summary')
    else:
        weather_preferences_form = WeatherPreferencesForm()
        health_conditions_form = HealthConditionsForm()

    context = {
        'weather_preferences_form': weather_preferences_form,
        'health_conditions_form': health_conditions_form,
    }
    return render(request, 'weatherpreferences/base_weather_questions.html', context)

def preference_summary(request):
    weather_preferences = WeatherPreferences.objects.get(user=request.user)
    health_conditions = HealthConditions.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'weather_preferences': weather_preferences,
        'health_conditions': health_conditions,
        'user_profile': user_profile,
    }
    return render(request, 'weatherpreferences/preference_summary.html', context)