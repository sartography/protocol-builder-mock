import os
basedir = os.path.abspath(os.path.dirname(__file__))

NAME = "CR Connect Protocol Builder Mock"
CORS_ENABLED = False
DEVELOPMENT = True
TESTING = False
SQLALCHEMY_DATABASE_URI = "postgresql://crc_user:crc_pass@localhost:5432/pb"
SECRET_KEY = 'a really really really really long secret key'
