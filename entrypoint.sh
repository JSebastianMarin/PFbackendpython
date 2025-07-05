#!/bin/bash

set -e

echo "Running Server"

echo "Migrating Database"
python manage.py makemigrations
python manage.py migrate

echo "Database setup completed"

gunicorn Movimientos_financieros.wsgi:application --bind 0.0.0.0:8000 --workers 2


