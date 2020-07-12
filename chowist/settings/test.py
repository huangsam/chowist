from chowist.settings.base import *  # noqa

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "circle_test",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "USERNAME": "circleci",
        "PASSWORD": "circleci",
    }
}
