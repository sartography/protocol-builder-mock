import re
import os
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))

NAME = "CR Connect Protocol Builder Mock"
CORS_ALLOW_ORIGINS = re.split(r',\s*', environ.get('CORS_ALLOW_ORIGINS', default="localhost:5000"))
DEVELOPMENT = True
TESTING = True
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', default="sqlite:///app.db")
SECRET_KEY = 'a really really really really long secret key'

print('### USING TESTING CONFIG: ###')
print('SQLALCHEMY_DATABASE_URI = ', SQLALCHEMY_DATABASE_URI)
print('TESTING = ', TESTING)
