from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('authenticate/', include('authenticate.urls')),
    path('forum/', include('forum.urls')),
    path('weatherapi/', include('weatherapi.urls')),
    path('weatherpreferences/', include('weatherpreferences.urls')),
    path('accounts/', include('allauth.urls')),
    path('marketing/', include('marketing.urls')),
    path('transactional/', include('transactional.urls')),
    path('django-admin/', admin.site.urls),  # Admin Django classique
    path('admin/', include(wagtailadmin_urls)),  # Admin Wagtail
    path('documents/', include(wagtaildocs_urls)),  # Docs Wagtail
    path('blog/', include(wagtail_urls)),  # Pages Wagtail (optionnel pour l’instant)
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
