# chowist

[![Build Status](https://travis-ci.org/huangsam/chowist.svg?branch=master)](https://travis-ci.org/huangsam/chowist)

Great places are chosen by great chowists.

This is an application that replicates core features of [Yelp](https://www.yelp.com/), and adds a couple more bells and whistles. A couple features/ideas that are in the process of being created:

- Chat sessions between users
- Homepage for marketing purposes
- Profile page for customization upon user login
- Ratings as aggregate views and detail views

## Getting started

Install the dependencies:

    pip install -r requirements.txt

Apply the database migrations:

    python manage.py migrate

Load sample data into the database:

    python manage.py loadsample data/places.json

### Development server

Start up the Django development server:

    python manage.py runserver

### Gunicorn workers

You can also consider running Gunicorn workers:

    gunicorn -w 4 chowist.wsgi

Just remember to host the static files somewhere like [Nginx](http://nginx.org/).

## How to contribute

Feel free to create pull requests to the following assets:

- Refine applications listed in `chowist.settings.INSTALLED_APPS`
- Add any restaurants you find into `data/places.json`
