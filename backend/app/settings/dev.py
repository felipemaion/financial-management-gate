from .base import *
from decouple import config, Csv

ALLOWED_HOSTS = []


INSTALLED_APPS += ['django_extensions']
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #'django.db.backends.sqlite3',
        'NAME': config('NAME'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
        'USER': config('DATABASEUSER'),
        'PASSWORD': config('PASSWORD'),
    }
}