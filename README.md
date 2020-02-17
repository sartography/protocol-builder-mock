
## Requirements
* Python 3
* pip (for python 3)
* pipenv (just run pip install pipenv)

## Running these examples
```bash
pipenv run python run.py
```
This will start a webserver on localhost at port 5001.  To see the api, you can visit
http://localhost:5001/pb/ui


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
