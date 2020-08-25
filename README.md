# Chowist

![](https://img.shields.io/circleci/build/github/huangsam/chowist)
![](https://img.shields.io/github/license/huangsam/chowist)

Great places are chosen by great chowists.

This is an application that replicates core features of [Yelp](https://www.yelp.com/), and adds a couple more bells and whistles.

Here are some key features:

- Homepage for marketing purposes
- Profile for customized experience
- Places as list and detail views

[Click here](https://youtu.be/SqVBcunjFHQ) to see a quick walkthrough of the application.

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

    python manage.py loaddemo .demo/places.json

Here are the loaded users for reference:

- `admin` with password `admin` (Super user)
- `john` with password `john` (Normal user)
- `jane` with password `jane` (Normal user)

### Docker setup

Complete local setup with Docker by running a single command:

    docker-compose -f compose/dev.yml -p chowist up --build -d

### Production setup

For production, you will want to use `gunicorn` for running the server:

    gunicorn -w 4 chowist.wsgi

When using Gunicorn, remember to host the static files from a web server.
