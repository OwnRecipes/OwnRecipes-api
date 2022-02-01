#!/usr/bin/env sh

# Install test related dependencies
pip install coveralls==3.3.1

# Prep the DB for testing
python3 manage.py reset_db --noinput
python3 manage.py migrate

# Run the tests and create a coverage report
coverage run --omit="*/migrations*,*/fixtures*" manage.py test -k
ret=$?
if [ $ret -ne 0 ]; then
    exit 1
fi

# Submit coverage to Coveralls
#coveralls
