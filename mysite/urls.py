from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authenticate.urls')),
    path('weather/', include('weatherapi.urls')),
]
