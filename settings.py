import os

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__))) + '/'

SECRET_KEY = 'django-insecure-tl2-=0-@b*e)xmg9z-u%f123ltjt8btz#7mwmmt#f$(ha^fqfg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
INSECURE = False
API_DOCUMENTATION = True
DEBUG_TOOLBAR = True
CLEAR_SEEN_JOKES = False

ALLOWED_HOSTS = ['*']

SITE_URL = 'joker'
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = None
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_hosts',
    'widget_tweaks',
    'django_tables2',
    'rest_framework',
    'django_filters',
    'drf_yasg2',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'core.Utils',
    'core.User',
    'core.Joke',
    'core.Privilege',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_DOMAIN = '.joker.local'
SESSION_COOKIE_DOMAIN = '.joker.local'

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'urls'
DEFAULT_HOST = 'public'
ROOT_HOSTCONF = 'hosts'

AUTH_USER_MODEL = 'User.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + 'core/templates/',
            BASE_DIR + 'Public/templates/',
            BASE_DIR + 'Admin/templates/',
            BASE_DIR + 'Api/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'joker',
        'USER': 'joker',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'htdocs')
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

CKEDITOR_UPLOAD_PATH = os.path.join(BASE_DIR, 'media/ckeditoruploads/')

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
    'admin': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Outdent', 'Indent',
             '-', 'Link', 'Unlink',
             'Format',
             ],
            ['HorizontalRule',
             '-', 'BulletedList', 'NumberedList',
             '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
             '-', 'SpecialChar',
             ],
            ['Maximize']
        ],
        'toolbarCanCollapse': True,
        'width': '100%',
    }
}

ITEMS_PER_PAGE = 20

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'Api.permissions.IsStaffUserPermission'
    ]
}

# celery
CELERY_RESULT_BACKEND = 'rpc'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_RESULT_EXPIRES = 60
CELERY_TASK_TIMEOUT = 10

# emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'healthcalendar.emailer@gmail.com'
DEFAULT_FROM_EMAIL = 'healthcalendar.emailer@gmail.com'
EMAIL_HOST_PASSWORD = '<PASSWORD OR SECURITY CODE OF APP>'

# senders
TELEGRAM_API_KEY = ''
TELEGRAM_API_HASH = ''
TELEGRAM_BOT_TOKEN = ''
TELEGRAM_SESSION_STORAGE_NAME = 'Joker'
TELEGRAM_BOT_NICKNAME = ''

HASHID_LENGTH = 64
HASHID_SECRET = ''

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CELERY_BEAT_SCHEDULE = {
    'send-everyday-joke-email': {
        'task': 'send-daily-jokes',
        'schedule': 60 * 60 * 24,  # 1 day
        'args': ('email',),  # core.joke.enums.SendMethods
        'options': {
            'expires': 60 * 60 * 1,  # 1h
        },
    },
    'send-everyday-joke-telegram': {
        'task': 'send-daily-jokes',
        'schedule': 60 * 60 * 24,  # 1 day
        'args': ('telegram_bot',),  # core.joke.enums.SendMethods
        'options': {
            'expires': 60 * 60 * 1,  # 1h
        },
    },
}


# from celery_runner import app
# from celery.schedules import crontab
#
# CELERY_TIMEZONE = 'UTC'
#
#
# app.conf.beat_schedule = {
#     'send-everyday-joke-email': {
#         'task': 'send-daily-jokes',
#         'schedule': crontab(hour=21, minute=35),
#         'args': ('email',),  # core.joke.enums.SendMethods
#         'options': {
#             'expires': 60 * 60 * 1,  # 1h
#         },
#     },
#     'send-everyday-joke-telegram': {
#         'task': 'send-daily-jokes',
#         'schedule': crontab(hour=21, minute=35),
#         'args': ('telegram_bot',),  # core.joke.enums.SendMethods
#         'options': {
#             'expires': 60 * 60 * 1,  # 1h
#         },
#     },
# }