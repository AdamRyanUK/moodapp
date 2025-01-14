from django.urls import path
from . import views

urlpatterns = [
    path('check_email/', views.check_email, name='check_email'),
]
