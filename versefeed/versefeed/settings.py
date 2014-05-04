"""
Django settings for versefeed project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tg+28=ym9tym2-a#$=yt-@r@hof21oj4v578mte6)(xj#c&td5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quiz',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
) 

ROOT_URLCONF = 'versefeed.urls'

WSGI_APPLICATION = 'versefeed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    
}

TEMPLATE_DIRS = (
'templates/',
)
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_ROOT = ''
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'public'),

    )

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



'''#authentication using social media and google using social auth extension'''

#First setup your base-line login urls
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/quiz/'
LOGIN_ERROR_URL = '/login-error/'

#Add social_auth to your INSTALLED_APPS
INSTALLED_APPS += (
    'social_auth', 
    )

#Add a new config setting which will define the authentication types you wish to support
AUTHENTICATION_BACKENDS = (
  'social_auth.backends.google.GoogleOAuth2Backend',
  'social_auth.backends.contrib.github.GithubBackend',
  'django.contrib.auth.backends.ModelBackend',
)

#Add social_auth as a template processor
TEMPLATE_CONTEXT_PROCESSORS += (
  "social_auth.context_processors.social_auth_by_type_backends",
)

#Some social_auth specific settings
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#social_auth backends
SOCIAL_AUTH_ENABLED_BACKENDS = ('google', 'github')

#Add your respective social API information.
GITHUB_API_KEY = ''
GITHUB_API_SECRET = ''
 
GOOGLE_OAUTH2_CLIENT_ID = '511202606770-qfpfq70ur49gh6ag1hn3hkgeu44jtlb9.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'U9qo7hO64pMcfrG7iexNeGtF'
