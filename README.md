# chowist

[![CircleCI](https://circleci.com/gh/huangsam/chowist.svg?style=svg)](https://circleci.com/gh/huangsam/chowist)

Great places are chosen by great chowists.

This is an application that replicates core features of [Yelp](https://www.yelp.com/), and adds a couple more bells and whistles.

Here are some key features:

- Homepage for marketing purposes
- Profile for customized experience
- Places as list and detail views

## Getting started

Here are some things to be aware of in development and production.

### Local setup

Install dependencies and create a `virtualenv` instance:

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Then run database migration:

    python manage.py migrate

Finally, start up the Django development server:

    python manage.py runserver

### Local data

For local development, you can load some data:

    python manage.py loaddata restaurant
    python manage.py loaddata user

Here are the loaded users for reference:

- `admin` with password `admin` (Super user)
- `john` with password `john` (Normal user)
- `jane` with password `jane` (Normal user)

**Note:** `DJANGO_SECRET` was set as `dummy` for proper user authentication.

### Docker setup

Complete local setup with Docker by running a single command:

    docker-compose -f compose/dev.yml -p chowist up --build -d

### Production setup

For production, you will want to use `gunicorn` for running the server:

    gunicorn -w 4 chowist.wsgi

When using Gunicorn, remember to host the static files from a web server.

## How to contribute

Feel free to create pull requests for the following:

- Enhancements to Django application logic
- Additional media content (`JPG`, `SVG`, etc.)
- Additional restaurants for `restaurant` fixture
