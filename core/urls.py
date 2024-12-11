from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('solutions', views.solutions, name="solutions"),
]
