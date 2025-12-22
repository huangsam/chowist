from chowist.settings.base import *  # noqa

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PORT": "5432",
    }
}


# Email Backend
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
