# import json
import os
import datetime

# with open('config.json') as config_file:
#     config = json.load(config_file)

class Config:
    # SQLALCHEMY_DATABASE_URI = config.get('DATABASE_URL')
    # SECRET_KEY = config.get('SECRET_KEY')
    # JWT_SECRET_KEY = config.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
