import os

class Config():
	DATABASE = {
		'HOST': os.environ['HOST'],
		'USER': os.environ['USER'],
		'PASSWORD': os.environ['PASSWORD'],
		'DBNAME': os.environ['DATABASE'],
	}

	SECRETS = {
		'GOOGLE_CONSUMER_KEY': os.environ.get('KEY'),
		'GOOGLE_CONSUMER_SECRET': os.environ.get('SECRET')
	}

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

	SECRETS = {
		'GOOGLE_CONSUMER_KEY': os.environ['KEY'],
		'GOOGLE_CONSUMER_SECRET': os.environ['SECRET']
	}

	from main import app
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disable signal to application when a change is made in database
	app.config['SQLALCHEMY_ECHO'] = True  # debugging purpose
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE['USER'] + ':' + DATABASE['PASSWORD'] + '@' \
	                                        + DATABASE['HOST'] + ':' + DATABASE['PORT'] + '/' + DATABASE['DBNAME']
