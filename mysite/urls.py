from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf import settings
from django.conf.urls.static import static
from core.views import custom_set_language

# URLs qui ne dépendent pas de la langue
urlpatterns = [
    path('django-admin/', admin.site.urls),  # Admin Django hors i18n
    path('admin/', include(wagtailadmin_urls)),  # Admin Wagtail hors i18n
    path('documents/', include(wagtaildocs_urls)),  # Docs Wagtail hors i18n
    path('set_language/', custom_set_language, name='set_language'),
]

# URLs avec préfixe de langue
urlpatterns += i18n_patterns(
    path('authenticate/', include('authenticate.urls')),
    path('forum/', include('forum.urls')),
    path('weatherapi/', include('weatherapi.urls')),
    path('weatherpreferences/', include('weatherpreferences.urls')),
    path('accounts/', include('allauth.urls')),
    path('marketing/', include('marketing.urls')),
    path('transactional/', include('transactional.urls')),
    path('blog/', include(wagtail_urls)),  # Pages Wagtail
    path('', include('core.urls')),  # Par défaut (core)
)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)