from pathlib import Path
import os

DEBUG = False

# if DEBUG:
#     from dotenv import load_dotenv
#     load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['ParsaJournal.liara.run',]
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS if host not in ['localhost', '127.0.0.1']]  # برای جلوگیری از CSRF errors
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Admin Security Settings
ADMIN_IP_WHITELIST = os.getenv('ADMIN_IP_WHITELIST', '').split(',') if os.getenv('ADMIN_IP_WHITELIST') else []
ADMIN_URL = os.getenv('ADMIN_URL', 'admin')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Must be after SessionMiddleware and before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_panel.middleware.AdminSecurityMiddleware',  # Custom admin security middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# PostgreSQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME',),
        'USER': os.getenv('DB_USER',),
        'PASSWORD': os.getenv('DB_PASSWORD',),
        'HOST': os.environ['DB_HOST'],
        'PORT': os.getenv('DB_PORT',),
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c timezone=Asia/Tehran',
        },
        'CONN_MAX_AGE': 600,  # Connection pooling: keep connections alive for 10 minutes
    }
}
# DATABASE_URL
DB_HOST = os.environ['DB_HOST']
# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Tehran'
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

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

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

LOGGING = {
    'version': 1,
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
    'django.request': {
        'handlers': ['console'],
        'level': 'ERROR',
        'propagate': False,
    },
}
}


# Pagination
PAGINATION_PER_PAGE = 10
