#!/bin/sh
python manage.py migrate
python manage.py loaddata restaurant user
python manage.py runserver 0.0.0.0:8000
