#!/bin/bash

# run migrations
export FLASK_APP=/app/pb/__init__.py

if [ "$DOWNGRADE_DB" = "true" ]; then
  echo 'Downgrading database...'
  poetry run flask db downgrade
fi

if [ "$UPGRADE_DB" = "true" ]; then
  echo 'Upgrading database...'
  poetry run flask db upgrade
fi

if [ "$RESET_DB" = "true" ]; then
  echo 'Clearing database and loading example data...'
  poetry run flask load-example-data
fi

if [ "$LOAD_EXAMPLE_SPONSORS" = "true" ]; then
  echo 'Loading example data...'
  poetry run flask load-example-sponsors
fi

if [ "$APPLICATION_ROOT" = "/" ]; then
  poetry run gunicorn --bind 0.0.0.0:$PORT0 wsgi:app
else
  poetry run gunicorn -e SCRIPT_NAME="$APPLICATION_ROOT" --bind 0.0.0.0:$PORT0 wsgi:app
fi
