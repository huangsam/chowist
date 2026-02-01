from chowist.settings.base import *  # noqa

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "github_test",
        "USER": "github",
        "PASSWORD": "github",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Cache configuration for testing
# Uses Redis in CI to match production caching behavior
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
