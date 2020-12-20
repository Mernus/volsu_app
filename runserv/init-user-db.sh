#!/bin/sh
set -e

psql -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --command "CREATE USER ${DB_USER} WITH SUPERUSER PASSWORD '${DB_PASSWORD}';" &&\
psql  -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --command "CREATE DATABASE ${DB_DATABASE} WITH OWNER ${DB_USER};" &&\
psql -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --command "CREATE EXTENSION citext;"