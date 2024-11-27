from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('update-location/', views.update_location, name='update_location'),
    path('location-history/', views.location_history, name='location_history'),
    path('my-history/', views.feedback_calendar_view, name='my_history'),
]
