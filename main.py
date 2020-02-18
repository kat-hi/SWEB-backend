import os
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS


DB = SQLAlchemy()
MA = Marshmallow()
admin = Admin()
login_manager = LoginManager()

def create_app():
	app = Flask('__main__')
	DB.init_app(app)  # initialize SQLAlchemy
	MA.init_app(app)  # initialize Marshmallow
	admin.init_app(app)
	login_manager.init_app(app)
	CORS(app)
	return app


def set_environment():
	app.app_context().push()
	from config import Config
	if os.environ['FLASK_ENV'] == 'dev':
		app.config.from_object('config.Config')
		print(app.config['SQLALCHEMY_DATABASE_URI'])
	else:
		app.config.from_object('config.Production')
		print(app.config['SQLALCHEMY_DATABASE_URI'])
	app.secret_key = Config.SECRETS['SECRET_KEY']


def create_tables():
	app.app_context().push()
	import models
	from admin import pflanzlistetable, obstsortentable, patentable
	admin.add_view(pflanzlistetable(models.Pflanzliste, DB.session))
	admin.add_view(obstsortentable(models.Sorten, DB.session))
	admin.add_view(patentable(models.Paten, DB.session))


app = create_app()
app.app_context().push()

set_environment()
logging.basicConfig(level=logging.DEBUG)

create_tables()

from login import admin_login
from api import api
app.register_blueprint(admin_login)
app.register_blueprint(api)


