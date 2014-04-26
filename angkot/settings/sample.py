from .common imoprt *

# Sentry config. Uncomment them if you use Sentry
# RAVEN_CONFIG = {
#     'dsn': '',
# }
# INSTALLED_APPS = INSTALLED_APPS + (
#     'raven.contrib.django.raven_compat',
# )
# LOGGING['root'] = {
#     'level': 'WARNING',
#     'handlers': ['sentry'],
# }
# LOGGING['handlers']['sentry'] = {
#     'level': 'DEBUG',
#     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'angkot',
#         'USER': 'angkot',
#         'PASSWORD': 'angkot',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# GOOGLE_ANALYTICS_IGNORE = False
# GOOGLE_ANALYTICS_ID = ''
# GOOGLE_ANALYTICS_HOST = ''
# MAPBOX_KEY = ''
# BING_MAPS_KEY = ''

# USERVOICE_KEY = ''
# USERVOICE_FORUM_ID = ''

ACCOUNT_USERNAME_PREFIX = 'user'
ANGKOT_CONTRIBUTOR_TERMS_URL = ''
ANGKOT_PRIVACY_POLICY_URL = ''

# Authentication keys from providers

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

