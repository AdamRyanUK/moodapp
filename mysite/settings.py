import os
import django_heroku
import dj_database_url
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# languages
USE_I18N = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),  # Répertoire pour vos fichiers de traduction
]
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
    ('es', 'Español'),
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=4kyj)60h7iy7)_3%djs%npl6*#*pc&-p(-)7pzr$4ae9c+-@z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'clearskyapp.herokuapp.com',  # Heroku domain
    'clearskyapp.io',             # Custom domain without "https://"
    'www.clearskyapp.io',         # Custom domain with "www"
    'clearsky-staging-app-f7ac40698cd6.herokuapp.com',  # Specific Heroku staging app domain
]


# Setting the default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# setting the fallback login url 

LOGIN_URL = '/accounts/login/' # Change this to your custom login URL
# where users are redirected after a sucessful login i.e. homepage

LOGIN_REDIRECT_URL = '/' 

# when the user does not refresh page
CSRF_FAILURE_VIEW = "core.views.csrf_failure_view"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'authenticate',
    'core',
    'weatherapi',
    'weatherpreferences',
    'forum',
    'marketing',
    'transactional',    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',  # wagtail.core est remplacé par wagtail depuis v2+
    'modelcluster',
    'taggit',
    'blog',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'weatherapi.middleware.ForecastMiddleware',
    'authenticate.middleware.FirstLoginMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mysite.context_processors.add_user_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

ENV = os.getenv('ENV')

if ENV == 'production':
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
    DEBUG = False
    # Add other production-specific settings here
elif ENV == 'staging':
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
    DEBUG = True
    # Add other staging-specific settings here
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    DEBUG = True
    # Add other development-specific settings here

WAGTAILADMIN_BASE_URL = "https://clearsky.io" #pour emails de reglage depuis wagtail pour le blog
WAGTAIL_SITE_NAME = "ClearSky"  # Nom de ton site, mets ce que tu veux
WAGTAIL_APPEND_SLASH = False
DEBUG = True

# Configuration AWS à partir des variables d'environnement
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')  # Récupère 'clearskyappfr' depuis Heroku
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')  # Valeur par défaut si non définie
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Configuration des médias pour Wagtail/Django
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
MEDIA_ROOT = ''  # Pas besoin avec S3

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#media files 
# Where uploaded images are stored
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core', 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())

# For local testing
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.protonmail.ch'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'admin@clearskyapp.io'
EMAIL_HOST_PASSWORD = 'NTDSEQ2KNG4HW1A7'
DEFAULT_FROM_EMAIL = 'admin@clearskyapp.io'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Clearsky '

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': config('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email',],
        'AUTH_PARAMS': {'access_type': 'online',}
    },
    'facebook': {
        'APP': {
            'client_id':config('FACEBOOK_APP_CLIENT_ID'),
            'secret': config('FACEBOOK_APP_SECRET'),
        },
        'METHOD': 'oauth2',  # Set to 'js_sdk' to use the Facebook connect SDK
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v17.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v17.0',
    }
}

SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

# Mailchimp settings 
MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY")  # 🔒 Récupère la clé API depuis Heroku
MAILCHIMP_MARKETING_AUDIENCE_ID = "e85afe938b"
MAILCHIMP_REGION = "us9"

MAILCHIMP_TRANSACTIONAL_API_KEY = os.getenv("MAILCHIMP_API_KEY")




