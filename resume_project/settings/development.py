from .base import *

DEGUB = True

INSTALLED_APPS += [

]


MIDDLEWARE += [

]


# In development -
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
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


# When testing 'DEBUG_TOOLBAR_ENABLED' should be 'False'. Otherwise: 'True'.
DEBUG_TOOLBAR_ENABLED = True
if DEBUG and DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    MIDDLEWARE.insert(1, 'django.middleware.cache.UpdateCacheMiddleware')
    MIDDLEWARE.append('django.middleware.cache.FetchFromCacheMiddleware')
    #INTERNAL_IPS.append('127.0.0.1')

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

    # https://gist.github.com/douglasmiranda/9de51aaba14543851ca3#gistcomment-3765183
