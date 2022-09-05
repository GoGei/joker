from settings import *


TEST = True
DEBUG = True
INSECURE = False
API_DOCUMENTATION = True
DEBUG_TOOLBAR = False


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_TEST_NAME'),
        'USER': os.environ.get('DATABASE_TEST_USER'),
        'PASSWORD': os.environ.get('DATABASE_TEST_PSW'),
        'HOST': os.environ.get('DATABASE_TEST_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_TEST_PORT', 5432),
        'ATOMIC_REQUESTS': True,
    }
}
