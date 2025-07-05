#!/bin/bash

echo "Running Server"

echo "Migrating Database"
python manage.py makemigrations
python manage.py migrate

echo "Database setup completed"

gunicorn --chdir /movimientos_financieros Movimientos_financieros.wsgi:application --bind 0.0.0.0:8000 --workers 2


