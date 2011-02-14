# Django settings for energyweb project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'energy',                      # Or path to database file if using sqlite3.
        'USER': 'energy',                      # Not used with sqlite3.
        'PASSWORD': 'energy',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# The following is used in energyweb for the static files.  It should
# be an absolute path to static/ .

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/local/energy/static/'

# The following is used in energyweb for the static files.

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=no!u@xf*45*z(48uo$^a(aw1jw*t23n2om^f+as#dc1tf1jml'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'energyweb.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/local/energy/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'energyweb.graph',
    # Uncomment the next line to enable the admin:
    #'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    #'django.contrib.databrowse',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'energyweb.graph.context_processors.media_url',
    'energyweb.graph.context_processors.nav_urls',
)


# Energyweb stuff.


# AVG_TYPES is a tuple of time periods over which readings will be
# averaged (the averages being stored in power_averages).  The values
# are strings, expected to correspond to the inputs to the PostgreSQL
# function date_trunc.  See:
# http://www.postgresql.org/docs/8.4/interactive/functions-datetime.html

MON_PID_FILE_TEMPL = '/var/local/energy/run/energymon.%d.pid'
MON_LOG_FILE_TEMPL = '/var/local/energy/log/energymon.%d.log'

FAKER_PID_FILE_TEMPL = '/var/local/energy/run/energyfaker.%d.pid'
FAKER_LOG_FILE_TEMPL = '/var/local/energy/log/energyfaker.%d.log'

FAKER_SLEEP_VARIATION = 0.1

LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'

# If a socket error is encountered, wait this many seconds before
# trying to reconnect.
ERROR_PAUSE = 9
