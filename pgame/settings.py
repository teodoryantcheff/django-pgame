"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# FIXME since the code has been on github this needs to be regenerated before production use
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '595n*bewz13po90=0ea4sv4yi9sc(le#70u9g4+d0*!=yn*iok'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# apps coming from django definition
DJANGO_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# non-django, 3rd party apps
THIRD_PARTY_APPS = (
    'custom_user',        # EmailUser
    'debug_toolbar',      # DjDT
    'django_extensions',  # django-extensions
    'solo',               # model singletons
    'account',            # django-user-accounts
    # 'axes',  # TODO django-axes
)

# Apps defined in the project
PROJECT_APPS = (
    'pgameapp',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'pgameapp.middleware.CastToCustomUserMiddleware',

    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',

    # 'axes.middleware.FailedLoginMiddleware',  # TODO django-axes
)
# #############
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # for django-admin-tools
    'django.core.context_processors.request',

    'account.context_processors.account',
    'pgameapp.context_processors.remote_ip',
    'pgameapp.context_processors.game_currency',
    'pgameapp.context_processors.game_statistics',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.auth_backends.EmailAuthenticationBackend',
)

##############
ROOT_URLCONF = 'pgame.urls'

WSGI_APPLICATION = 'pgame.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'pgame.sqlite3'),
    }
}


# Email settings
EMAIL_HOST = ''
EMAIL_PORT = 0
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'user@domain.com'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


AUTH_USER_MODEL = 'custom_user.EmailUser'
# AUTH_USER_MODEL = 'pgameapp.User'


# django-accounts
# see http://django-user-accounts.readthedocs.org/en/latest/ for full parameter set
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = True
ACCOUNT_LOGIN_REDIRECT_URL = '/'
ACCOUNT_USER_DISPLAY = lambda user: user.email


# Crypto wallet config
CRYPTO_WALLET_PROTO = ''
CRYPTO_WALLET_IP = ''
CRYPTO_WALLET_PORT = 0
CRYPTO_WALLET_USER = ''
CRYPTO_WALLET_PASSWORD = ''


# for django debug toolbar
INTERNAL_IPS = ('127.0.0.1', '192.168.0.10')

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingDebugPanel',
)


# axes
# AXES_LOGIN_FAILURE_LIMIT: The number of login attempts allowed before a record is created for the failed logins. Default: 3
# AXES_LOCK_OUT_AT_FAILURE: After the number of allowed login attempts are exceeded, should we lock out this IP (and optional user agent)? Default: True
# AXES_USE_USER_AGENT: If True, lock out / log based on an IP address AND a user agent. This means requests from different user agents but from the same IP are treated differently. Default: False
# AXES_COOLOFF_TIME: If set, defines a period of inactivity after which old failed login attempts will be forgotten. Can be set to a python timedelta object or an integer. If an integer, will be interpreted as a number of hours. Default: None
# AXES_LOGGER: If set, specifies a logging mechanism for axes to use. Default: 'axes.watch_login'
# AXES_LOCKOUT_TEMPLATE: If set, specifies a template to render when a user is locked out. Template receives cooloff_time and failure_limit as context variables. Default: None
# AXES_LOCKOUT_URL: If set, specifies a URL to redirect to on lockout. If both AXES_LOCKOUT_TEMPLATE and AXES_LOCKOUT_URL are set, the template will be used. Default: None
# AXES_VERBOSE: If True, you'll see slightly more logging for Axes. Default: True
# AXES_USERNAME_FORM_FIELD: the name of the form field that contains your users usernames. Default: username

try:
    from local_settings import *
except:
    pass