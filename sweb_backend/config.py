import os
from oauthlib.oauth2 import WebApplicationClient


class Config():
	DATABASE = {
		'HOST': os.environ['HOST'],
		'USER': os.environ['USER'],
		'PASSWORD': os.environ['DB_PASSWORD'],
		'DBNAME': os.environ['DATABASE'],
	}

	SECRETS = {
		'GOOGLE_CLIENT_ID': os.environ.get('GOOGLE_CLIENT_ID', None),
		'GOOGLE_CLIENT_SECRET': os.environ.get('GOOGLE_CLIENT_SECRET', None),
		'SECRET_KEY': os.environ.get("SECRET_KEY"),
	}

	LOGIN = {
		'ADMIN_EMAIL_1': os.environ['ADMIN_EMAIL_1'],
		'ADMIN_EMAIL_2': os.environ['ADMIN_EMAIL_2'],
		'CLIENT': WebApplicationClient(SECRETS['GOOGLE_CLIENT_ID']),
		'GOOGLE_DISCOVERY_URL': os.environ['GOOGLE_DISCOVERY_URL'],
		'ADMIN_BASE_URL': os.environ['ADMIN_BASE_URL']
	}

	SMTP = {
		'PORT': os.environ['SMTP_PORT'],
		'SERVER': os.environ['SMTP_SERVER'],
		'SENDER': os.environ['SENDER_EMAIL'],
		'RECEIVER': os.environ['RECEIVER_EMAIL'],
		'PASSWORD': os.environ['SMTP_PASSWORD']
	}

	IMAGE_BASE_URL = os.environ['IMAGE_BASE_URL']

	from main import app
	app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable signal to application when a change is made in database
	app.config['SQLALCHEMY_ECHO'] = True  # debugging purpose
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE['USER'] + ':' + DATABASE['PASSWORD'] + '@' \
	                                        + DATABASE['HOST'] + '/' + DATABASE['DBNAME']
	

class Production(Config):
	DATABASE = {
		'HOST': os.environ['MYSQL_ROOT_HOST'],
		'USER': os.environ['MYSQL_USER'],
		'PASSWORD': os.environ['MYSQL_PASSWORD'],
		'DBNAME': os.environ['MYSQL_DATABASE'],
		'PORT': os.environ['MYSQL_PORT']
	}

	from main import app
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable signal to application when a change is made in database
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE['USER'] + ':' + DATABASE['PASSWORD'] + '@' \
	                                        + DATABASE['HOST'] + ':' + DATABASE['PORT'] + '/' + DATABASE['DBNAME']