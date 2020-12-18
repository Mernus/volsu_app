#!/bin/bash

if [ "$1" == "uwsgi" ]; then
    echo "Running migrations"
    python manage.py migrate --noinput
    echo "Running collectstatic"
    python manage.py collectstatic --noinput
    echo "Starting project"
    uwsgi runserv/uwsgi.ini
    exit
fi

exec "$@"