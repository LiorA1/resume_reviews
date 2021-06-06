
from .base import *


import django_heroku
#DEBUG = False
DEBUG_TOOLBAR_ENABLED = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
ALLOWED_HOSTS = ['*']

STATICFILES_DIRS = [
    #os.path.join(BASE_DIR, "staticfiles"),
]


django_heroku.settings(locals())