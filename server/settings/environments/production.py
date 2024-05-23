"""
This file contains all the settings used in production.

This file is required and if development.py is present these
values are overridden.
"""

from server.settings.components import config
import os.path

# Production flags:
# https://docs.djangoproject.com/en/2.2/howto/deployment/

DEBUG = False

ALLOWED_HOSTS = [
    # TODO: check production hosts
    config('DOMAIN_NAME'),

    # We need this value for `healthcheck` to work:
    'localhost',
    '0.0.0.0',
]

CSRF_TRUSTED_ORIGINS = [
    "https://" + config('DOMAIN_NAME'),
    "http://" + config('DOMAIN_NAME'),
    ]

# Staticfiles
# https://docs.djangoproject.com/en/2.2/ref/contrib/staticfiles/

# This is a hack to allow a special flag to be used with `--dry-run`
# to test things locally.
_COLLECTSTATIC_DRYRUN = config(
    'DJANGO_COLLECTSTATIC_DRYRUN', cast=bool, default=False,
)
# Adding STATIC_ROOT to collect static files via 'collectstatic':
STATIC_ROOT = '.static' if _COLLECTSTATIC_DRYRUN else '/var/www/django/static'

STATICFILES_DIRS: List[str] = [
    os.path.join('static'),

]

STATIC_URL = "/static/"


# Media files
# https://docs.djangoproject.com/en/2.2/topics/files/

MEDIA_ROOT = '/var/www/django/media'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

_PASS = 'django.contrib.auth.password_validation'  # noqa: S105
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': '{0}.UserAttributeSimilarityValidator'.format(_PASS)},
    {'NAME': '{0}.MinimumLengthValidator'.format(_PASS)},
    {'NAME': '{0}.CommonPasswordValidator'.format(_PASS)},
    {'NAME': '{0}.NumericPasswordValidator'.format(_PASS)},
]


# Security
# https://docs.djangoproject.com/en/2.2/topics/security/

CSP_SCRIPT_SRC = (
    "'self'",
    'ajax.googleapis.com',
    'cdnjs.cloudflare.com',
    'maxcdn.bootstrapcdn.com',
    'cdn.jsdelivr.net',
)
CSP_IMG_SRC = (
    "'self'",
    'data:'
)
CSP_CONNECT_SRC = (
    "'self'",
)
CSP_FONT_SRC = (
    "'self'",
    'fonts.gstatic.com',
    'maxcdn.bootstrapcdn.com',
    'netdna.bootstrapcdn.com',
    'cdn.jsdelivr.net',
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'fonts.googleapis.com',
    'maxcdn.bootstrapcdn.com',
    'netdna.bootstrapcdn.com',
    'cdn.jsdelivr.net',
)


SECURE_HSTS_SECONDS = 10  # the same as Caddy has
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SECURE_REDIRECT_EXEMPT = [
    # This is required for healthcheck to work:
    '^health/',
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
