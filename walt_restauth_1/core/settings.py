import os
from pathlib import Path

import dotenv
dotenv.load_dotenv()

from django.core.exceptions import ImproperlyConfigured

def get_env_setting(setting, default=None):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]

    except KeyError:
        if default is not None:
            return default
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = get_env_setting('SECRET_KEY')

DEBUG = get_env_setting('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '[::1]']

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    #'core.accounts.models.EmailBackend',
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

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'stmp.mailgun.com'
EMAIL_HOST_USER = 'postmaster@mg.kokserek.site'
EMAIL_HOST_PASSWORD = 'c7f75ba47c9f4ab85b4710ab16c01a33-8889127d-b78a0f8f'

EMAIL_CONFIRM_REDIRECT_BASE_URL = 'http://localhost:3000/email/confirm/'
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = 'http://localhost:3000/password-reset/confirm/'

INSTALLED_APPS = [
    'django.contrib.admin', # This app provides the Django administration interface, allowing to manage application's data through a web-based interface.
    'django.contrib.auth', # Provides the authentication system for handling user authentication, permissions, and user groups.
    'django.contrib.contenttypes', # Enables content types, which are used to track models' types and their relationships in a generic way.
    'django.contrib.sessions', # Handles user sessions and allows you to store and retrieve arbitrary data on a per-site-visitor basis.
    'django.contrib.messages', # Allows to store and display one-time messages (e.g., flash messages) for users.
    'django.contrib.staticfiles', # Collect and serves static files, such as CSS, JavaScript, and images.

    'django.contrib.sites', # Provides a framework for handling multiple sites from a single Django installation.

    'allauth', # This third-party app provides an integrated set of authentication and registration functionalities for handling user sign-up, login, and password management.
    'allauth.account', # An extension of allauth that handles user account management, including email confirmation and password change.
    'allauth.socialaccount', # An extension of allauth that allows users to authenticate via social media accounts.
    'allauth.socialaccount.providers.facebook', # A provider for allauth.socialaccount that enables Facebook authentication.
    'allauth.socialaccount.providers.github', # A provider for allauth.socialaccount that enables GitHub authentication.

    'phonenumber_field', # Adds support for phone number fields to your models.

    'dj_rest_auth', # Provides RESTful API endpoints for authentication using Django Rest Framework.
    'dj_rest_auth.registration', # An extension of dj_rest_auth that handles user registration through RESTful API endpoints.

    'rest_framework', # For building Web APIs using Django, providing features like serializers, views, and authentication.
    'rest_framework.authtoken', # An extension of rest_framework that enables token-based authentication for API requests.
    'rest_framework_simplejwt', # Another extension of rest_framework that provides JSON Web Token (JWT) authentication for API requests.

    'core.accounts', # Custom app specific to this project, providing additional account-related functionality.
    'core.employers', # Another custom app specific to this project, dealing with employer-related functionality.
    'core.jobseekers', # A custom app specific to this project, likely focused on jobseeker-related functionality.
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

REST_USE_JWT = True

SITE_ID = int(os.environ.get('SITE_ID', 1))

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_setting('POSTGRES_DB'),
        'USER': get_env_setting('POSTGRES_USER'),
        'PASSWORD': get_env_setting('POSTGRES_PASSWORD'),
        'HOST': get_env_setting('POSTGRES_HOST'),
        'PORT': int(get_env_setting('POSTGRES_PORT', '5432'))
    }
}

# DATABASES['default']['TEST'] = {
#     'NAME': 'waltdatabase',
# }

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
