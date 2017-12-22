#to start mysql -> mysql-ctl cli
#mysql database name = etes_db

import os
SECRET_KEY = 'you-will-never-guess'
DEBUG=True
DB_USERNAME = 'tqtruong95'
DB_PASSWORD = '' # not required for cloud9
ETES_DATABASE_NAME = 'etes_db'
DB_HOST = os.getenv('IP', '0.0.0.0')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, ETES_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
# UPLOAD_FOLDER = '/static/uploads'
