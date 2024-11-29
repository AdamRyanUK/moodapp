from django.urls import path
from django.http import HttpResponse

def placeholder_view(request):
    return HttpResponse("Weather API is Under Construction.")

urlpatterns = [
    path('', placeholder_view, name='placeholder'),  # Placeholder URL pattern
]
