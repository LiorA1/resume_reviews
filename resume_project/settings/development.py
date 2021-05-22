from .base import *

DEGUB = True

INSTALLED_APPS += [
    #'el_pagination',
]

MIDDLEWARE += [

]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
