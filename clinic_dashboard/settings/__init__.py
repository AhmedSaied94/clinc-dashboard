"""
Settings package initialization.
Automatically loads the appropriate settings module based on DJANGO_ENV environment variable.
"""
import os
from decouple import config

# Determine which settings module to use
ENVIRONMENT = config('DJANGO_ENV', default='dev')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'dev':
    from .dev import *
else:
    from .dev import *
