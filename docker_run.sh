#!/bin/bash

# run migrations
export FLASK_APP=./app.py
pipenv run flask db upgrade
pipenv run python ./run.py
