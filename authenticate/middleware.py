from django.shortcuts import redirect
from django.urls import reverse

class FirstLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.first_login:
                excluded_paths = [reverse('register_weather_preferences'), '/weatherapi/city-autocomplete/']
                # Check if path is in excluded paths or starts with /admin
                if request.path not in excluded_paths and not request.path.startswith('/admin'):
                    return redirect('register_weather_preferences')
        response = self.get_response(request)
        return response

class RegistrationCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
from django.utils import timezone
from datetime import datetime, timedelta
