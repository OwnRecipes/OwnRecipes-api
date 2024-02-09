#!/usr/bin/env sh

BASEDIR=/opt/ownrecipes/ownrecipes-api

# Activate python virtualenv
. $BASEDIR/bin/activate

# Update the DB if it needs it and compile static files.
python3 $BASEDIR/manage.py migrate --no-input
python3 $BASEDIR/manage.py collectstatic --no-input

# Start up gunicorn
bash $BASEDIR/base/gunicorn_start.sh
