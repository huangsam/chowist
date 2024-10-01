from chowist.settings.base import *  # noqa

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "USERNAME": "postgres",
        "PASSWORD": "postgres",
    }
}
