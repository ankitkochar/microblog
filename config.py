# chapter 3
# import os

# class Config(object):
# 	SECRET_KEY=os.environ.get("SECRET_KEY") or "ankit"

import os
import psycopg2
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	# ...
	SECRET_KEY=os.environ.get("SECRET_KEY") or "ankit"
	DATABASE_URL = "postgres://ahbyxztkbcjwpe:f6fb76ddb8d6901bfa399bade5a9aea1d118d61db965727f1be121f3597f18ec@ec2-54-145-224-156.compute-1.amazonaws.com:5432/d2uvedofabgdrn"
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	# mysql://username:password@localhost/db_name
	# pymysql+mysql://username:password@localhost/db_name
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mysql+pymysql://root:Ankit@123@localhost:3306/app"
	SQLALCHEMY_DATABASE_URI = "postgresql://ahbyxztkbcjwpe:f6fb76ddb8d6901bfa399bade5a9aea1d118d61db965727f1be121f3597f18ec@ec2-54-145-224-156.compute-1.amazonaws.com:5432/d2uvedofabgdrn"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = os.environ.get('MAIL_SERVER') or "smtp.googlemail.com"
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
	# MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "ankitkochar456@gmail.com"
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "ankit123"
	ADMINS = ['ankitkochar456@gmail.com']
	POSTS_PER_PAGE = 3
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')