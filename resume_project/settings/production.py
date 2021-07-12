
from .base import *


import django_heroku
DEBUG = False
DEBUG_TOOLBAR_ENABLED = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
ALLOWED_HOSTS = ['*']


# TODO: Add email backend
# ! Email Backend is not defined, because its require more resources.
# EMAIL EXAMPLE -
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
# More in:
# https://docs.djangoproject.com/en/3.2/topics/email/


# TODO: Add cache
# ! Cache is not defined, because its require more resources.
# More in:
# https://docs.djangoproject.com/en/3.2/topics/cache/


django_heroku.settings(locals())
