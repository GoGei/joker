from settings import *

DEBUG = True
INSECURE = False
API_DOCUMENTATION = True
DEBUG_TOOLBAR = True

TEMPLATES[0]['OPTIONS']['debug'] = True

SECRET_KEY = '<YOUR KEY>'

DATABASES['default']['USER'] = '<DB USER NAME>'
DATABASES['default']['PASSWORD'] = '<DB USER PASSWORD>'

# url options
SITE_URL = 'joker.local'
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = '1111'
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


GRAPH_MODELS['all_applications'] = [app for app in INSTALLED_APPS if app.startswith('core.')]
