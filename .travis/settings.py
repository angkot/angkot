from .common import *

# Sentry config. Uncomment them if you use Sentry
RAVEN_CONFIG = {
    'dsn': 'udp://u:p@localhost:9001/2',
}
INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)
LOGGING['root'] = {
    'level': 'DEBUG',
    'handlers': ['sentry'],
}
LOGGING['handlers']['sentry'] = {
    'level': 'DEBUG',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_angkot',
        'USER': 'angkot',
        'PASSWORD': 'angkot',
        'HOST': 'localhost',
        'PORT': '',
    }
}

GOOGLE_ANALYTICS_ID = 'UA-00000000-1'
GOOGLE_ANALYTICS_HOST = 'angkot.web.id'
GOOGLE_MAPS_KEY = 'google-maps-key'
MAPBOX_KEY = 'mapbox-key'
BING_MAPS_KEY = 'bingmaps-key'

USERVOICE_CODE = 'uservoice-code'

ALLOWED_HOSTS = ['angkot.web.id']

DEBUG = False
TEMPLATE_DEBUG = False

ACCOUNT_USERNAME_PREFIX = 'user'
ANGKOT_CONTRIBUTOR_TERMS_URL = 'https://github.com/fajran/angkot/wiki/Ketentuan-Kontribusi-(Rangkuman)'
ANGKOT_PRIVACY_POLICY_URL = 'https://github.com/fajran/angkot/wiki/Kebijakan-Privasi'

# Authentication keys from providers

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'google-oauth2-client-id'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'google-oauth2-client-secret'

SOCIAL_AUTH_FACEBOOK_KEY = 'facebook-app-id'
SOCIAL_AUTH_FACEBOOK_SECRET = 'facebook-api-secret'

SOCIAL_AUTH_TWITTER_KEY = 'twitter-consumer-key'
SOCIAL_AUTH_TWITTER_SECRET = 'twitter-consumer-secret'

# Logging

LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'formatter': 'basic',
    'class': 'logging.FileHandler',
    'filename': '/tmp/angkot-console.log',
}
LOGGING['handlers']['exception'] = {
    'level': 'ERROR',
    'formatter': 'exception',
    'filters': ['require_debug_false'],
    'class': 'logging.FileHandler',
    'filename': '/tmp/angkot-exception.log',
}

