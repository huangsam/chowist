from chowist.settings.base import *  # noqa

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

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
