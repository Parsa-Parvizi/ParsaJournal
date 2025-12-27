from pathlib import Path
import os
# import dj_database_url
# import loadenv from loadenv
import environ


# BASE_DIR = Path(__file__).resolve().parent.parent / 'Journal'
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)
env.read_env(str(BASE_DIR / '.env'))

DEBUG = True
# Security Settings
SECRET_KEY = env('DJANGO_SECRET_KEY')

ROOT_URLCONF = 'config.urls'


# BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    # 'whitenoise.runserver_nostatic',
    
    # Local apps
    'admin_panel',
    'core',
    'accounts',
    'articles',
    'reviews',
    'newsletter',
    'comments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Must be after SessionMiddleware and before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_panel.middleware.AdminSecurityMiddleware',  # Custom admin security middleware
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': ['core.templatetags.core_extras'],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',  # Adds LANGUAGE_CODE to context
                'core.context_processors.site_info',
            ],
        },
    },
]

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Tehran'

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL')
#     )
# }

USE_I18N = True
USE_TZ = True

# Internationalization
LANGUAGES = [
    ('fa', 'Persian'),
    ('en', 'English'),
]

# Site ID for sitemaps
SITE_ID = 1

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
# EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
# EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
# EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@parsajournal.ir')

# # Cache Configuration (Redis recommended for production; fallback to LocMem)
# CACHES = {
#     'default': {
#         'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.redis.RedisCache'),
#         'LOCATION': os.getenv('CACHE_LOCATION', 'redis://127.0.0.1:6379/1'),  # تنظیم کن اگر Liara Redis بده
#         'TIMEOUT': int(os.getenv('CACHE_TIMEOUT', 300)),
#         'OPTIONS': {
#             'MAX_ENTRIES': int(os.getenv('CACHE_MAX_ENTRIES', 1000)),
#         }
#     }
# }

# Session Configuration
# SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', 1209600))  # 2 weeks
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'  # پیش‌فرض True برای HTTPS
# SESSION_SAVE_EVERY_REQUEST = True

# Security Settings (فعال برای production)
# SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', 31536000))  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# LOGGING = {
#     'version': 1,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'INFO',
#     },
#     'loggers': {
#     'django.request': {
#         'handlers': ['console'],
#         'level': 'ERROR',
#         'propagate': False,
#         },
#     }
# }


# Pagination
PAGINATION_PER_PAGE = 10
