from django.urls import path
from . import views

urlpatterns = [
    path('edit_hometown/', views.edit_hometown, name='edit_hometown'),
]
