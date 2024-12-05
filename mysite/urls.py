from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('authenticate/', include('authenticate.urls')),
    path('weatherapi/', include('weatherapi.urls')),
    path('weatherpreferences/', include('weatherpreferences.urls')),
]
