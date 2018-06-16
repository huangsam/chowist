#!/bin/bash

python manage.py migrate
python manage.py loaddata places/restaurant.json
python manage.py runserver 0.0.0.0:8000
