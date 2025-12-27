import os

env = os.environ.get('DJANGO_ENV', 'local')

if env == 'production':
    from .production import *
elif env == 'staging':
    from .staging import *
else:
    from .local import *