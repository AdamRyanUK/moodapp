from django.shortcuts import redirect
from django.urls import reverse

class FirstLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'userprofile') and request.user.userprofile.first_login:
                if request.path != reverse('register_weather_preferences'):
                    return redirect('register_weather_preferences')
        response = self.get_response(request)
        return response
