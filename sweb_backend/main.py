import os
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_admin import Admin
from flask import Flask
from flask_login import LoginManager
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

DB = SQLAlchemy()
MA = Marshmallow()
AD = Admin(template_mode='bootstrap3')
login_manager = LoginManager()

def create_app():
	app = Flask(__name__)
	DB.init_app(app)
	MA.init_app(app)
	AD.init_app(app)
	login_manager.init_app(app)
	return app


def set_config_settings():
	app.app_context().push()
	from .config import Config, Production
	app.config['FLASK_ADMIN_SWATCH'] = 'spacelab'
	if os.environ['FLASK_ENV'] == 'dev':
		app.config.from_object(Config())
		print(app.config['SQLALCHEMY_DATABASE_URI'])
	else:
		app.config.from_object(Production())
		print(app.config['SQLALCHEMY_DATABASE_URI'])
	app.secret_key = Config.SECRETS['SECRET_KEY']


def create_admin_tables():
	app.app_context().push()
	from . import models
	from .admin_views import pflanzlistetable, obstsortentable, imagetable
	AD.add_view(imagetable(models.Image, DB.session))
	AD.add_view(pflanzlistetable(models.Plantlist, DB.session))
	AD.add_view(obstsortentable(models.Sorts, DB.session))


def register_all_blueprints():
	app.app_context().push()
	from .login import admin_login
	from .api import api
	app.register_blueprint(admin_login)
	app.register_blueprint(api)


app = create_app()
limiter = Limiter(
	app,
	key_func=get_remote_address,
	default_limits=['200 per day']
)

set_config_settings()
create_admin_tables()
register_all_blueprints()
logging.basicConfig(level=logging.DEBUG)


