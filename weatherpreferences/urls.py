# weatherpreferences/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('location-history/', views.location_history, name='location_history'), 
    path('feedback-calendar/', views.feedback_calendar_view, name='feedback_calendar'),
    path('register-weather-preferences/', views.register_weather_preferences, name='register_weather_preferences'),
    path('preference-summary/', views.preference_summary, name='preference-summary'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),    
    ]
