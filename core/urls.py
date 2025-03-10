from django.urls import path
from . import views
from .views import remove_city
from django.views.i18n import set_language 

urlpatterns = [
    path('set_language/', set_language, name='set_language'),
    path('', views.home, name="home"),
    path('mood-forecast-graph', views.mood_forecast_graph, name="mood-forecast-graph"),
    path('calendar', views.calendar_view, name="calendar"),
    path('insights', views.insights, name="insights"),
    path('remove_city/<int:city_id>/', remove_city, name='remove_city'),
    path('feedback-anomaly-data', views.feedback_anomaly_data, name='feedback-anomaly-data'),
    path('feedback-chart-data', views.feedback_chart_data, name='feedback-chart-data'),
    path('vacation', views.vacation_submit, name='vacation'),
    path('locations', views.location_display, name='locations'),
    path('weather-profile', views.weather_profile, name='weather-profile'),
]
