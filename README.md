# chowist

[![Build Status](https://travis-ci.org/huangsam/chowist.svg?branch=master)](https://travis-ci.org/huangsam/chowist)

Great places are chosen by great chowists.

This is an application that aims to replicate some features of **Yelp** while adding a little more bells and whistles. A couple of features/ideas that are in the process of being created:

- Chat sessions between users
- Homepage for marketing purposes
- Profile page for customization upon user login
- Ratings as aggregate views and detail views

## Getting Started

Install the dependencies:

    pip install -r requirements.txt

Apply the database migrations:

    python manage.py migrate

Load sample data into the database:

    python manage.py loadsample data/places.json

Start up the Django development server:

    python manage.py runserver

You can also consider running Gunicorn workers:

    gunicorn -w 4 chowist.wsgi

Just remember to host the static files somewhere like `Nginx`.
