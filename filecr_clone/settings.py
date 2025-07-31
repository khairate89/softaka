import os
from pathlib import Path
import environ # Make sure you have `pip install django-environ`
import cloudinary

# Initialize environ
env = environ.Env(
    # Set casting and default value for DEBUG
    DEBUG=(bool, False) # DEBUG will default to False if not set in env
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file for local development
# In production on Render, these will be loaded directly from Render's env vars

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

CLOUDINARY = {
    'cloud_name': env('CLOUDINARY_CLOUD_NAME'),
    'api_key': env('CLOUDINARY_API_KEY'),
    'api_secret': env('CLOUDINARY_API_SECRET'),
}

cloudinary.config(
    cloud_name=CLOUDINARY['cloud_name'],
    api_key=CLOUDINARY['api_key'],
    api_secret=CLOUDINARY['api_secret'],
    secure=True,
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY') # Loaded from environment variable

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG') # Loaded from environment variable (defaults to False)

# ALLOWED_HOSTS for Render
# Render provides your service's external hostname.
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost']) # For local dev


# Use Cloudinary for media files storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Application definition
INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'software',
    'nested_admin',
    'ckeditor_uploader',
    'ckeditor',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- Add Whitenoise middleware here, right after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # <--- Keep this here for i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'software.middleware.ForceAdminEnglishMiddleware',
]

ROOT_URLCONF = 'filecr_clone.urls' # Confirmed this is correct based on your previous input

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'software.context_processors.menu_categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'filecr_clone.wsgi.application' # Confirmed this is correct

# Database
# Use DATABASE_URL from environment for production (PostgreSQL)
# Fallback to SQLite for local development
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'), ('fr', 'Français'), ('de', 'Deutsch'),
    ('es', 'Español'), ('ar', 'العربية'), ('ru', 'Русский'), ('zh-hans', '中文'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Collect static files here
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'software', 'static'), # Ensure this path is correct
    # os.path.join(BASE_DIR, 'static'), # If you have a general project-level 'static' folder
]


# Media files (for user-uploaded content) - REMEMBER THIS WON'T PERSIST ON RENDER!
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # Local storage, not suitable for production uploads

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': 'codesnippet',
    },
    'description_toolbar': {
        'toolbar': [
            ['Source', '-', 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks'],
            ['Youtube','CodeSnippet','Preview','Print','-','Undo','Redo'],
            ['Find','Replace','-','SelectAll','-','Scayt']
        ],
        'extraPlugins': 'codesnippet,youtube',
        'height': 400,
        'width': '100%',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF_TRUSTED_ORIGINS: Important for forms if you're using a custom domain
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
if not DEBUG: # Add Render's internal URL and your custom domains in production
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
        CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')
    # Add your custom domains here if you use them, e.g.,
    # CSRF_TRUSTED_ORIGINS.append('https://yourdomain.com')


# Logging (as you had it)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'software.middleware': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
