#!/bin/bash

/bin/bash -ac 'cd /opt/ownrecipes/ownrecipes-api; . .env.service.local; exec python3 manage.py flushexpiredtokens'
