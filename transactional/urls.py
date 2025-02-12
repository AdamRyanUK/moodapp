from django.urls import path

from . import views

urlpatterns = [
    path('ping/', views.mailchimp_transactional_ping_view),  
    path('send/', views.send_view, name='mailchimp-send'),
]