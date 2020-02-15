from main import DB
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from flask_login import UserMixin

Base = automap_base()
Base.prepare(DB.engine, reflect=True)

from main import app
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)
app.app_context().push()

Pflanzliste = Base.classes.pflanzliste

'''
| id           | int(11)      | PRI   
| reihenID     | int(11)      | 
| reihenPos    | int(11)      |
| baumID       | int(11)      |
| baumsortenID | int(11)      |
| fruchtID     | int(11)      |
| frucht       | varchar(22)  |
| sortenID     | int(11)      | FK
| sorte        | varchar(100) |
| longitude    | double       |
| latitude     | double       |
| pate         | varchar(100) |
'''
Sorten = Base.classes.obstsorten
'''
| id           | int(11)      | PRI  
| fruchtID     | int(11)      |
| frucht       | varchar(100) |
| sorte        | varchar(100) |
| andereNamen  | varchar(255) |
| herkunft     | varchar(512) |
| groesse      | varchar(255) |
| beschreibung | varchar(512) |
| reifezeit    | varchar(255) |
| geschmack    | varchar(255) |
| verwendung   | varchar(512) |
| lager        | varchar(512) |
| verbreitung  | varchar(255) |
'''

Paten = Base.classes.paten

'''
+----------------+--------------+------+-----+
| id             | int(10)      | NO   | PRI 
| name           | varchar(100) | YES  |     
| vorname        | varchar(100) | YES  |     
| eintragUrkunde | varchar(100) | YES  |     
| mitpaten       | varchar(100) | YES  |     
| firma          | varchar(100) | YES  |   
| datum          | varchar(100) | YES  |       
| plz            | int(10)      | YES  |     
| ort            | varchar(100) | YES  |     
| tel            | varchar(100) | YES  |     
| email          | varchar(100) | YES  |     
| patenbaum      | varchar(100) | YES  |     
| entscheidung   | varchar(100) | YES  |    
| start          | varchar(100) | YES  |      
| ende           | varchar(100) | YES  |     
| baumId         | int(10)      | YES  |     
| urkunde        | varchar(100) | YES  |     
| followUp       | varchar(100) | YES  |     
| foto           | varchar(100) | YES  |     
| zahlart        | varchar(100) | YES  |     
| zahlfreq       | varchar(100) | YES  |     
| zahlbeginn     | varchar(100) | YES  |     
| zahlende       | varchar(100) | YES  |     
| quelle         | varchar(100) | YES  |     
| kommentar      | varchar(255) | YES  |     
'''


class Admin(DB.Model, UserMixin):
	__tablename__ = 'admins'
	id = DB.Column(DB.String, primary_key=False)
	email = DB.Column(DB.String, primary_key=True)
	authenticated = DB.Column(DB.String, default="false")
	active = DB.Column(DB.String, default="true")


def is_active(self):
	"""True, as all users are active."""
	if self.active == "true":
		return True


def get_id(self):
	"""Return the email address to satisfy Flask-Login's requirements."""
	return self.email


def is_authenticated(self):
	"""Return True if the user is authenticated."""
	if self.authenticated == "true":
		return True


def is_anonymous(self):
	"""False, as anonymous users aren't supported."""
	return False

