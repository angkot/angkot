"""
Django settings for angkot project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1(t!amm#)n2wdyo^wk2w)*6xbj)e-wg=i5&i64!49o97f_(a91'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',

    'social.apps.django_app.default',

    'south',
    'reversion',
    'django_hstore',

    'angkot.route',
    'angkot.account',
    'angkot.page',
    'angkot.line',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'angkot.account.middleware.AngkotSocialAuthExceptionMiddleware',
    'angkot.middleware.ExceptionLoggerMiddleware',
)

ROOT_URLCONF = 'angkot.urls'

WSGI_APPLICATION = 'angkot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'angkot',
        'USER': 'angkot',
        'PASSWORD': 'angkot',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'id-id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = ''

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = ''

MEDIA_URL = ''


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'angkot.context_processors.configs',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)s %(levelname)s - %(message)s'
        },
        'basic-user': {
            'format': '%(asctime)s %(name)s %(levelname)s - %(uid)s/%(user)s - %(message)s'
        },
        'exception': {
            'format': '%(asctime)s %(name)s %(levelname)s - %(message)s'
        },
        'exception-user': {
            'format': '%(asctime)s %(name)s %(levelname)s - %(uid)s/%(user)s - %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
        'console-user': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic-user',
        },
        'exception': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'exception',
        },
        'exception-user': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'exception-user',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'angkot': {
            'handlers': ['console-user'],
            'level': 'INFO',
        },
        'angkot.middleware.ExceptionLoggerMiddleware': {
            'handlers': ['exception'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

AUTHENTICATION_BACKENDS = (
    'angkot.account.backends.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
     'social.pipeline.social_auth.social_details',
     'social.pipeline.social_auth.social_uid',
     'social.pipeline.social_auth.auth_allowed',
     'social.pipeline.social_auth.social_user',
     'angkot.account.user.get_username',
     'social.pipeline.user.create_user',
     'social.pipeline.social_auth.associate_user',
     'social.pipeline.social_auth.load_extra_data',
     'social.pipeline.user.user_details'
)

ANGKOT_CONTRIBUTOR_TERMS_URL = ''
ANGKOT_PRIVACY_POLICY_URL = ''

LOGIN_REDIRECT_URL = '/account/'
LOGIN_ERROR_URL = '/account/login/+fail/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/account/login/+ok/'

SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = [
    'ao', # auth origin - where the auth starts
    'aos', # auth origin section - more detailed location
]
SOCIAL_AUTH_FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'popup'}

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

