import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "tests"
BROKER_PASSWORD = "tests"
BROKER_VHOST = "tests-vhost"

CELERY_ALWAYS_EAGER = True
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_ERROR_EMAILS = True

CELERYD_LOG_LEVEL = 'INFO'
CELERYD_POOL = "eventlet"
CELERYD_CONCURRENCY = 10

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Victor Poluceno', 'victorpoluceno@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rest_api',
        'USER': 'tests',
        'PASSWORD': 'tests',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

SECRET_KEY = '671y85xk@_vh!(#*5c^c1(#&r#oz=)4nskjxx*)sr+f-9ru+0c'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'djcelery',
    'django_jenkins',
    'rest_api',
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'core.rest_api': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },

    }
}
