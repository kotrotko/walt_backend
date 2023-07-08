#import sys
import os
from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-wlwnz6*j#ov)qyyvtrhst_ht79n8ou_d&e_j=r%ik@7hzeb%lq'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '[::1]']

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    #'walt_restauth_1.accounts.models.EmailBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
#EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'stmp.mailgun.com'
EMAIL_HOST_USER = 'postmaster@mg.kokserek.site'
EMAIL_HOST_PASSWORD = 'c7f75ba47c9f4ab85b4710ab16c01a33-8889127d-b78a0f8f'

EMAIL_CONFIRM_REDIRECT_BASE_URL = 'http://localhost:3000/email/confirm/'
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = 'http://localhost:3000/password-reset/confirm/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',

    'django_extensions',
    'phonenumber_field',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    'walt_restauth_1.accounts',
    'walt_restauth_1.employers',
    'walt_restauth_1.jobseekers',
]

LOGIN_URL = 'http://localhost:8000/accounts/login'
LOGIN_REDIRECT_URL = 'home'

SOCIALACCOUNT_PROVIDERS = {
    'facebook':
        {'METHOD': 'oauth2',
         'SCOPE': ['email'],
         'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
         'LOCALE_FUNC': lambda request: 'en_US',
         'VERSION': 'v13.0'
         },
    'github': {
        'APP': {
            'client_id': '4f1d7d548d4102a7f973',
            'secret': 'f4adb32bd32b12ca70b136c507c017a4b32dd0f6',
        }
    },
    'google':
        {},
    'twitter':{}
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAdminUser'
    ],
}

# REST_AUTH = {
#     'USE_JWT': True,
#     'JWT_AUTH_COOKIE': '',
#     'JWT_AUTH_REFRESH_COOKIE': '',
# }
#REGISTER_SERIALIZER

REST_USE_JWT = True

SITE_ID = 1

# JWT_AUTH_COOKIE = 'walt_restauth_1'
# JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'

ROOT_URLCONF = 'walt_restauth_1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'walt_restauth_1.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
