import os

INSTALLED_APPS = [
    'accounts',
    'chat',
]

DEBUG = os.environ.get('DEBUG', False)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

APP_HOST = os.environ.get('HOST', '0.0.0.0')
APP_PORT = os.environ.get('PORT', 80)

# Database url

DATABASE_URL = os.environ.get('DATABASE_URL', '')

# Static files
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')


# Rdis settings
REDIS = 'localhost', 6379


# Template dir path
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


from .local_settings import *