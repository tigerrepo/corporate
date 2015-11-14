"""
Django settings for tiger project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b8y&pvt)jkiuh%9l#lmowl@ysz(^e79j6c2r&ou$eyk556f0kr'

# SECURITY WARNING: don't run with debug turned on in production!
import datetime

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['www.riceglobal.com']

COUNTRY = 'SG'

# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tiger',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# TEMPLATE_CONTEXT_PROCESSORS = (
    # "django.contrib.auth.context_processors.auth",
    # "django.core.context_processors.debug",
    # "django.core.context_processors.i18n",
    # "django.core.context_processors.media",
    # "django.core.context_processors.static",
    # "django.core.context_processors.tz",
    # "django.contrib.messages.context_processors.messages",
# )

ROOT_URLCONF = 'tiger.urls'

WSGI_APPLICATION = 'tiger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'corporate',
        'USER': 'root',
        'PASSWORD' : '123456',
        'HOST':'',
        'PORT':3306,
    }
}

STATIC_URL = '/static/'
DOMAIN_NAME = 'http://www.riceglobal.com/'
IMAGE_URL_PREFIX = 'http://cdn.riceglobal.com/gallery/'
MEDIA_ROOT = '/var/www/cdn.riceglobal.com/gallery/'
MEDIA_URL = '%s' % IMAGE_URL_PREFIX
PDF_URL = 'http://cdn.riceglobal.com/pdf/'
VIDEO_URL = 'http://cdn.riceglobal.com/video/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(MEDIA_ROOT, "static"),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    os.path.join(BASE_DIR, 'templates'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '%(asctime)s|%(levelname)s|%(process)d:%(thread)d|%(filename)s:%(lineno)d|%(module)s.%(funcName)s|%(message)s',
        },
        'short' : {
            'format': '%(asctime)s|%(levelname)s|%(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/riceglobal/web.log.%s' % (datetime.datetime.now().date(),),
            'formatter':'standard',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


PAGE_COUNT = 3
YOUTUBE_URL_PREFIX = 'http://www.youtube.com/embed/'

LANGUAGE_CODE = 'en'
LANGUAGES = (
  ('en', 'English'),
  ('zh_CN', 'Chinese'),
)

