from chowist.settings.base import *  # noqa

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "chowist",
        "USER": "chowist",
        "PASSWORD": "chowist",
        "HOST": "db",
        "PORT": "5432",
    }
}


# Cache configuration for development
# Uses Redis for better performance and persistence
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # Use service name in Docker Compose
    }
}


# Email Backend
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
