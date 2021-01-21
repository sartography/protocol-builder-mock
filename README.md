# sartography/protocol-builder-mock

# UVA IRB Protocol Builder Mock

## Requirements
* Python 3
* pip (for python 3)
* pipenv (just run pip install pipenv)

## Database Setup
The database for the CR Connect project will create an empty database for protocol builder as well.
We did this because you would only by running this mock in order to support the app.  Would be good
to have this set up and run as a part of that docker-compose rather than having to spin this up seperately.

With the database running, be sure to execute

```
flask db upgrade
```
to set up the database structure.


## Starting up Protocol Builder
```bash
pipenv run python run.py
```
This will start a webserver on localhost at port 5001.  To see the api, you can visit
http://localhost:5001/pb/ui

## Create an example study
Finally, you will need to connect to the protocol builder mock ui in a web browser (see above url)
And use this to connect to create a new study.  Be sure the study is owned by the person you are logging in
to on CR-Connect.  For must development environments this will be dhf8r.


## For future reference, these are the steps Sartography is taking to set up Mock Services:

1. mdkir project
1. cd project
1. pipenv install
1. pipenv install flask
1. pipenv install connexion
1. place your swagger/openapi file in the root directory
1. add methods to return example data in the app.py file.

## Deploying to staging
We don't have a travis / test environment set up for this yet, no tests
but you can build and publish it with:
```bash
docker image build -t sartography/protocol-builder-mock:latest .
docker push sartography/protocol-builder-mock:latest
```
