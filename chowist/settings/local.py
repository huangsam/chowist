import os

from chowist.settings.base import *  # noqa

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Email Backend
# https://docs.djangoproject.com/en/3.0/topics/email/#email-backends
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
