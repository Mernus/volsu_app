#!/bin/bash
set -e

BOLD="\033[1m"
NC="\033[0m"

if [ "$1" == "uwsgi" ]; then
    printf "${BOLD} [ENTRYPOINT | INFO] Initialize project. ${NC} \n"
    python manage.py initialize
    printf "${BOLD} [ENTRYPOINT | INFO] Generating tests data. ${NC} \n"
    python manage.py generate_test_data
    printf "${BOLD} [ENTRYPOINT | INFO] Set admin interface. ${NC}"
    python manage.py loaddata admin_interface_theme_bootstrap.json
    printf "${BOLD} [ENTRYPOINT | INFO] Starting project. ${NC} \n"
    uwsgi runserv/uwsgi.ini
    exit
fi

exec "$@"