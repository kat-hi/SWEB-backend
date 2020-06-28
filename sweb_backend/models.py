from sqlalchemy.ext.automap import automap_base
from flask_login import UserMixin
from sqlalchemy import create_engine
from .main import DB

Base = automap_base()
Base.prepare(DB.engine, reflect=True)

from .main import app

app.app_context().push()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True, pool_size=5)
engine.connect()


class Plantlist(DB.Model):
	__tablename__ = 'pflanzliste'
	BaumNr = DB.Column(DB.Integer, primary_key=True)
	Pflanzreihe = DB.Column(DB.Integer)
	PflanzreihePosition = DB.Column(DB.Integer)
	BaumID = DB.Column(DB.Integer)
	BaumsortenID = DB.Column(DB.Integer)
	FruchtID = DB.Column(DB.Integer)
	Frucht = DB.Column(DB.String)
	SortenID = DB.Column(DB.Integer)
	Sortenzaehler = DB.Column(DB.Integer)
	Sorte = DB.Column(DB.String)
	Ernte = DB.Column(DB.Float)
	PatenID = DB.Column(DB.String)
	Longitude = DB.Column(DB.Float)
	Latitude = DB.Column(DB.Float)


class Sorts(DB.Model):
	__tablename__ = 'obstsorten'
	id = DB.Column(DB.Integer, primary_key=True)
	fruchtID = DB.Column(DB.Integer)
	frucht = DB.Column(DB.String)
	sorte = DB.Column(DB.String)
	andereNamen = DB.Column(DB.String)
	herkunft = DB.Column(DB.String)
	groesse = DB.Column(DB.String)
	beschreibung = DB.Column(DB.String)
	reifezeit = DB.Column(DB.String)
	geschmack = DB.Column(DB.String)
	verwendung = DB.Column(DB.String)
	lager = DB.Column(DB.String)
	verbreitung = DB.Column(DB.String)


class Admins(DB.Model, UserMixin):
	__tablename__ = 'admins'
	id = DB.Column(DB.String, primary_key=False)
	email = DB.Column(DB.String, primary_key=True)
	authenticated = DB.Column(DB.String, default="false")
	active = DB.Column(DB.String, default="true")


class Image(DB.Model):
	__tablename__ = 'Bilder'
	id = DB.Column(DB.Integer, primary_key=True)
	uri = DB.Column(DB.String)


def is_active(self):
	"""True, as all users are active."""
	app.logger.info('IS ACTIVE ' + str(self.active))
	if self.active == "true":
		return True


def get_id(self):
	"""Return the email address to satisfy Flask-Login's requirements."""
	app.logger.info('GET ID ' + str(self.email))
	return self.email


def is_authenticated(self):
	"""Return True if the user is authenticated."""
	app.logger.info('IS AUTHENTICATED' + str(self.authenticated))
	if self.authenticated == "true":
		return True


def is_anonymous(self):
	"""False, as anonymous users aren't supported."""
	return False

