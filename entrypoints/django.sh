#!/bin/sh
set -euxo pipefail

# Apply db migrations against database
python manage.py migrate

# Load demo data for the places app
python manage.py loaddemo .demo/places.json

# Start the development server
python manage.py runserver 0.0.0.0:8000
