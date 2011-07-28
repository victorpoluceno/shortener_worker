import os, json

envfilepath = os.path.join(os.environ['HOME'], 'environment.json')
environment = json.load(open(envfilepath))

import djcelery
djcelery.setup_loader()

BROKER_HOST = environment['DOTCLOUD_QUEUE_AMQP_HOST']
BROKER_PORT = environment['DOTCLOUD_QUEUE_AMQP_PORT']
BROKER_USER = environment['DOTCLOUD_QUEUE_AMQP_LOGIN']
BROKER_PASSWORD = environment['DOTCLOUD_QUEUE_AMQP_PASSWORD']
#BROKER_USE_SSL = True

CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_SEND_EVENTS = True
#CELERY_RESULT_BACKEND = "cache"
#CELERY_CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

CELERYD_LOG_LEVEL = 'INFO'
CELERYD_SOFT_TASK_TIME_LIMIT = 180
CELERYD_POOL = "eventlet"
CELERYD_CONCURRENCY = 10

# set CELERY_ALWAYS_EAGER=True before running tests
TEST_RUNNER = 'djcelery.contrib.test_runner.run_tests' 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Victor Poluceno', 'victorpoluceno@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'template1',
        'USER': environment['DOTCLOUD_DB_SQL_LOGIN'],
        'PASSWORD': environment['DOTCLOUD_DB_SQL_PASSWORD'],
        'HOST': environment['DOTCLOUD_DB_SQL_HOST'],

        # use str() to ensure no unicode string on python 2.6 
        # because psycopg doesnt like it
        'PORT': str(environment['DOTCLOUD_DB_SQL_PORT']),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = '671y85xk@_vh!(#*5c^c1(#&r#oz=)4nskjxx*)sr+f-9ru+0c'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'djcelery',
    'gateway_backend',
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
        'gateway_backend': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },

    }
}
