"""
Development settings for clinic_dashboard project.
"""

from .base import *
from .logging import *

DEBUG = True

# Database
# Using SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email backend for development - prints to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Development-specific middleware
INSTALLED_APPS += [
    # Add django-debug-toolbar if needed later
]

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# Disable some security features for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
