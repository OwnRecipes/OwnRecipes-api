#!/usr/bin/env sh

# Update the DB if it needs it and compile static files.
/code/manage.py migrate --no-input
/code/manage.py collectstatic --no-input

# Start cron service
/usr/sbin/crond -b

# Start up gunicorn
/code/base/gunicorn_start.sh
