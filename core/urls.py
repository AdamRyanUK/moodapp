from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('insights', views.insights, name="insights"),
    path('journal', views.mood_journal, name="journal"),
]
