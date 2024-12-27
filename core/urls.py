from django.urls import path
from . import views
from .views import remove_city

urlpatterns = [
    path('', views.home, name="home"),
    path('calendar', views.calendar_view, name="calendar"),
    path('insights', views.insights, name="insights"),
    path('remove_city/<int:city_id>/', remove_city, name='remove_city'),
]
