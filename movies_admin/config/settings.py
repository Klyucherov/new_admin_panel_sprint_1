import os
from pathlib import Path

from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get("DEBUG", default=True)

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

include(
    'components/inst_app.py',
)

include(
    'components/middleware.py',
)

ROOT_URLCONF = 'config.urls'

include(
    'components/templates.py',
)

WSGI_APPLICATION = 'config.wsgi.application'

include(
    'components/database.py',
    optional('local_settings.py')
)

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

STATIC_URL = 'static/'

LANGUAGE_CODE = 'ru-RU'
LOCALE_PATHS = ['movies/locale']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
