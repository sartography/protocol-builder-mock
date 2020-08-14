#!/bin/bash

# run migrations
export FLASK_APP=/app/pb/__init__.py

if [ "$DOWNGRADE_DB" = "true" ]; then
  echo 'Downgrading database...'
  pipenv run flask db downgrade
fi

if [ "$UPGRADE_DB" = "true" ]; then
  echo 'Upgrading database...'
  pipenv run flask db upgrade
fi

if [ "$RESET_DB" = "true" ]; then
  echo 'Clearing database and loading example data...'
  pipenv run flask load-example-data
fi

if [ "$LOAD_EXAMPLE_SPONSORS" = "true" ]; then
  echo 'Loading example data...'
  pipenv run flask load-example-sponsors
fi

if [ "$APPLICATION_ROOT" = "/" ]; then
  pipenv run gunicorn --bind 0.0.0.0:$PORT0 wsgi:app
else
  pipenv run gunicorn -e SCRIPT_NAME="$APPLICATION_ROOT" --bind 0.0.0.0:$PORT0 wsgi:app
fi
