# chowist

[![Build Status](https://travis-ci.com/huangsam/chowist.svg?branch=master)](https://travis-ci.com/huangsam/chowist)

Great places are chosen by great chowists.

This is an application that replicates core features of [Yelp](https://www.yelp.com/), and adds a couple more bells and whistles. A couple features/ideas that are in the process of being created:

- Homepage for marketing purposes
- Profile settings upon user login
- Places as list and detail views

## Getting started

Here are some things to be aware of in development and production.

### Local setup

Install dependencies and create a `virtualenv` instance:

    pipenv install
    pipenv shell

Then run database migration:

    python manage.py migrate

Finally, start up the Django development server:

    python manage.py runserver

For development, you might want test data to validate the app's functionality:

    python manage.py loaddata restaurant user

This loads restaurants and an `admin` user with password `admin`. The `admin` user allows you to enter the Django dashboard and view users/groups/data in a consolidated view.

**Note:** `DJANGO_SECRET` must be set to `dummy` for the `admin` user to work. Otherwise, you will need to create a new superuser with `python manage.py createsuperuser`.

#### Dockerized setup

To finish the complete local setup with Docker:

    docker-compose -f compose/dev.yml -p chowist up --build -d

### Production setup

For production, you might want to use `gunicorn` for running the server:

    gunicorn -w 4 chowist.wsgi

When using Gunicorn, remember to host the static files from a web server.

## How to contribute

Feel free to create pull requests to the following assets:

- Update Django application logic
- Update media content (`JPG`, `SVG`, etc.)
- Add restaurants into `restaurant.json`
