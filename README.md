# chowist [![Build Status](https://travis-ci.org/huangsam/chowist.svg?branch=master)](https://travis-ci.org/huangsam/chowist) Great places are chosen by great chowists.

This is an application that replicates core features of [Yelp](https://www.yelp.com/), and adds a couple more bells and whistles. A couple features/ideas that are in the process of being created:

- Homepage for marketing purposes
- Profile settings upon user login
- Places as list and detail views

## Getting started

Run the following commands:

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py loaddata places/data.json

Finally, start up the Django development server:

    python manage.py runserver

Or a set of Gunicorn servers:

    gunicorn -w 4 chowist.wsgi

When using Gunicorn, remember to host the static files from a web server.

## How to contribute

Feel free to create pull requests to the following assets:

- Update Django application logic
- Update media content (CSS/JPG/SVG/etc.)
- Add restaurants into `places/data.json`
