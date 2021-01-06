import re
import os
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))

NAME = "CR Connect Protocol Builder Mock"
FLASK_PORT = environ.get('PORT0') or environ.get('FLASK_PORT', default="5001")
CORS_ALLOW_ORIGINS = re.split(r',\s*', environ.get('CORS_ALLOW_ORIGINS', default="localhost:5000"))
DEVELOPMENT = environ.get('DEVELOPMENT', default="true") == "true"
TESTING = environ.get('TESTING', default="false") == "true"

# Add trailing slash to base path
APPLICATION_ROOT = re.sub(r'//', '/', '/%s/' % environ.get('APPLICATION_ROOT', default="/").strip('/'))

DB_HOST = environ.get('DB_HOST', default="localhost")
DB_PORT = environ.get('DB_PORT', default="5432")
DB_NAME = environ.get('DB_NAME', default="pb")
DB_USER = environ.get('DB_USER', default="crc_user")
DB_PASSWORD = environ.get('DB_PASSWORD', default="crc_pass")
SQLALCHEMY_DATABASE_URI = environ.get(
    'SQLALCHEMY_DATABASE_URI',
    default="postgresql://%s:%s@%s:%s/%s" % (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
)
SECRET_KEY = environ.get('SECRET_KEY', default='a really really really really long secret key')

LDAP_URL = 'mock'
# LDAP_URL = 'ldap.virginia.edu'
LDAP_TIMEOUT_SEC = 10

print('=== USING DEFAULT CONFIG: ===')
print('DB_HOST = ', DB_HOST)
print('CORS_ALLOW_ORIGINS = ', CORS_ALLOW_ORIGINS)
print('DEVELOPMENT = ', DEVELOPMENT)
print('TESTING = ', TESTING)
print('APPLICATION_ROOT = ', APPLICATION_ROOT)
