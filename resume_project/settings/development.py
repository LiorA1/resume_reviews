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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'cache:11211',
    }
}


INTERNAL_IPS = [

]


DEBUG_TOOLBAR_ENABLED = True
if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS.append('127.0.0.1')

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False if request.is_ajax() else True,
}
 
 # https://gist.github.com/douglasmiranda/9de51aaba14543851ca3#gistcomment-3765183