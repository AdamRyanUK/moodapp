from django.urls import path
from . import views

urlpatterns = [
    path('user_details/', views.user_details, name='user-details'),
]
