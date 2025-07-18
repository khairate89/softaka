from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-test-key'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'software',
    'nested_admin',
    'ckeditor_uploader',
    'ckeditor',
    'django.contrib.humanize',
]

# filecr_clone_django_project/filecr_clone_django_project/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cookie.CookieMiddleware', # Only if you explicitly added it. SessionMiddleware usually handles cookies.

    'django.middleware.locale.LocaleMiddleware', # <--- MOVE IT TO THIS POSITION!

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'software.middleware.ForceAdminEnglishMiddleware', # Your custom middleware should generally be last or near last
]

ROOT_URLCONF = 'filecr_clone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # <-- ADD THIS LINE
        
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required for admin & i18n
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'software.context_processors.menu_categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'filecr_clone.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
    ('de', 'Deutsch'),
    ('es', 'Español'),
    ('ar', 'العربية'),
    ('ru', 'Русский'),
    ('zh-hans', '中文'),
]


LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'software' / 'static']
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CKEDITOR_UPLOAD_PATH = "uploads/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/' # Files will be uploaded to MEDIA_ROOT/uploads/
CKEDITOR_IMAGE_BACKEND = 'pillow' # Ensure Pillow is installed: pip install Pillow (if not already)

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': 'codesnippet',
    },
    'description_toolbar': { # A custom toolbar for description
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
    # You can define more custom toolbars for different fields if needed
}

# settings.py (at the very end of the file)
print(f"BASE_DIR: {BASE_DIR}")
print(f"MEDIA_ROOT: {MEDIA_ROOT}")
print(f"STATIC_ROOT: {STATIC_ROOT}") # Just for completeness

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
        'level': 'INFO', # Set to INFO to see our middleware messages
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Add a logger for your middleware module
        'software.middleware': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}