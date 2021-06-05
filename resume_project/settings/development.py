from .base import *

DEGUB = True

INSTALLED_APPS += [
    #'el_pagination',
    'debug_toolbar',
    
]



MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'cache:11211',
    }
}


INTERNAL_IPS = [

]



DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False if request.is_ajax() else True,
}
 