#!/bin/sh

# Apply db migrations against database
python manage.py migrate

# Load test data for restaurants and users
python manage.py loaddata restaurant user

# Start the development server
python manage.py runserver 0.0.0.0:8000
