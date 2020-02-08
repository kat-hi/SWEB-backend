import os
from oauthlib.oauth2 import WebApplicationClient

# .env provides all env-variables that are used by production or development mode
class Config():
	DATABASE = {
		'HOST': os.environ['HOST'],
		'USER': os.environ['USER'],
		'PASSWORD': os.environ['PASSWORD'],
		'DBNAME': os.environ['DATABASE'],
	}

	SECRETS = {
		'GOOGLE_CLIENT_ID': os.environ.get("GOOGLE_CLIENT_ID", None),
		'GOOGLE_CLIENT_SECRET': os.environ.get("GOOGLE_CLIENT_SECRET", None),
		'SECRET_KEY': os.environ.get("SECRET_KEY")

	}

	CLIENT = WebApplicationClient(SECRETS['GOOGLE_CLIENT_ID'])
	GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

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
	app.config['SQLALCHEMY_ECHO'] = True  # debugging purpose
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE['USER'] + ':' + DATABASE['PASSWORD'] + '@' \
	                                        + DATABASE['HOST'] + ':' + DATABASE['PORT'] + '/' + DATABASE['DBNAME']
