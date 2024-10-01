from chowist.settings.base import *  # noqa

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "github",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "USERNAME": "github",
        "PASSWORD": "github_test",
    }
}

print("DB config for test env - ", DATABASES)
