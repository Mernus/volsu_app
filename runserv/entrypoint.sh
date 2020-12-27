#!/bin/bash
set -e

if [ "$1" == "uwsgi" ]; then
    echo "Running migrations"
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    echo "Running collectstatic"
    python manage.py collectstatic --noinput
    echo "Set admin interface"
    python manage.py loaddata admin_interface_theme_bootstrap.json
    echo "Starting project"
    uwsgi runserv/uwsgi.ini
    exit
fi

exec "$@"