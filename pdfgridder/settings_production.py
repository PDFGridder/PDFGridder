import os

from .settings import *

# Django settings for website project.

DEBUG = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = '/home/pdfgridder/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/site_media/static/admin/'
AVATAR_GRAVATAR_BASE_URL = 'https://secure.gravatar.com/avatar/'
AVATAR_AUTO_GENERATE_SIZES = (16, 80,)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 0,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ALLOWED_HOSTS = ['.pdfgridder.org']

CELERY_ALWAYS_EAGER = False

CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
STATIC_URL = 'https://pdfgridder.org/site_media/static/'
