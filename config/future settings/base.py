# from pathlib import Path
# import environ

# BASE_DIR = Path(__file__).resolve().parent.parent.parent

# env = environ.Env(
#     DEBUG=(bool, False)
# )

# # بارگذاری فایل env در local فقط
# if env.bool("USE_DOTENV", default=False):
#     environ.Env.read_env(BASE_DIR / ".env.local")

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sitemaps',
#     'django.contrib.sites',
#     'whitenoise.runserver_nostatic',
    
#     # Local apps
#     'admin_panel',
#     'core',
#     'accounts',
#     'articles',
#     'reviews',
#     'newsletter',
#     'comments',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.locale.LocaleMiddleware',  # Must be after SessionMiddleware and before CommonMiddleware
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'admin_panel.middleware.AdminSecurityMiddleware',  # Custom admin security middleware
# ]

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'builtins': ['core.templatetags.core_extras'],
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'django.template.context_processors.i18n',  # Adds LANGUAGE_CODE to context
#                 'core.context_processors.site_info',
#             ],
#         },
#     },
# ]

# AUTH_USER_MODEL = 'accounts.User'

# LANGUAGE_CODE = 'en'
# TIME_ZONE = 'Asia/Tehran'