# weatherpreferences/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('location-history/', views.location_history, name='location_history'), 
    path('register-weather-preferences/', views.register_weather_preferences, name='register_weather_preferences'),
    path('preference-summary/', views.preference_summary, name='preference-summary'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),   
    path('check-feedback-status/', views.check_feedback_status, name='check-feedback-status'), 
    path('journal', views.mood_journal, name="journal"),
    path('action-questions', views.action_questions, name="action_questions"),
    ]
