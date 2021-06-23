import re
import os
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))

NAME = "CR Connect Protocol Builder Mock"
CORS_ALLOW_ORIGINS = re.split(r',\s*', environ.get('CORS_ALLOW_ORIGINS', default="localhost:5000"))
DEVELOPMENT = True
TESTING = True
DB_HOST = environ.get('DB_HOST', default="localhost")
DB_PORT = environ.get('DB_PORT', default="5432")
DB_NAME = environ.get('DB_NAME', default="pb_test")
DB_USER = environ.get('DB_USER', default="crc_user")
DB_PASSWORD = environ.get('DB_PASSWORD', default="crc_pass")
SQLALCHEMY_DATABASE_URI = environ.get(
    'SQLALCHEMY_DATABASE_URI',
    default="postgresql://%s:%s@%s:%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
)

SECRET_KEY = 'a really really really really long secret key'
WTF_CSRF_ENABLED = False

print('### USING TESTING CONFIG: ###')
print('SQLALCHEMY_DATABASE_URI = ', SQLALCHEMY_DATABASE_URI)
print('TESTING = ', TESTING)
