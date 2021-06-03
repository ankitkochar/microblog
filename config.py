# chapter 3
# import os

# class Config(object):
# 	SECRET_KEY=os.environ.get("SECRET_KEY") or "ankit"

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
	SECRET_KEY=os.environ.get("SECRET_KEY") or "ankit"
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
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