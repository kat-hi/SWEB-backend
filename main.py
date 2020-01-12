from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import simplejson
from flask_admin import Admin
from flask_cors import CORS, cross_origin
import os

DB = SQLAlchemy()
MA = Marshmallow()
admin = Admin()


def create_app():
	app = Flask('__main__')
	DB.init_app(app)  # initialize SQLAlchemy
	MA.init_app(app)  # initialize Marshmallow
	admin.init_app(app)
	CORS(app)
	return app


app = create_app()

from config import Config, Production

if os.environ['FLASK_ENV'] == 'dev':
	config_settings = Config()
	app.config.from_object(config_settings)  # get development config settings
	app.config['SQLALCHEMY_DATABASE_URI'] = config_settings.SQLALCHEMY_DATABASE_URI
	print(config_settings.SQLALCHEMY_DATABASE_URI)
else:
	config_settings = Production()
	app.config.from_object(config_settings)  # get production config settings
	app.config['SQLALCHEMY_DATABASE_URI'] = config_settings.SQLALCHEMY_DATABASE_URI
	print(config_settings.SQLALCHEMY_DATABASE_URI)

from admin import pflanzlistetable, obstsortentable, patentable
import models


def create_tables():
	app.app_context().push()
	admin.add_view(pflanzlistetable(models.Pflanzliste, DB.session))
	admin.add_view(obstsortentable(models.Sorten, DB.session))
	admin.add_view(patentable(models.Paten, DB.session))


create_tables()


@app.route('/api', methods=['GET'])
@cross_origin(origin='localhost:3000/')
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	return response


@app.route('/api/karte', methods=['GET'])
@cross_origin(origin='localhost:3000/karte')
def infos():
	global DB
	import models, schemas
	tree_results = DB.session.query(models.Pflanzliste).all()
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	tree_schema = schemas.Tree(many=True)
	trees_output = tree_schema.dump(tree_results)
	return simplejson.dumps(trees_output, ensure_ascii=False, encoding='utf8'), 200


@app.route('/api/karte/baeume', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume')
def get_trees():
	global DB
	import models, schemas
	sorten_results = DB.session.query(models.Sorten).all()
	if not sorten_results:
		return jsonify({'message': 'No entry found'}), 400
	sorten_schema = schemas.Sorten(many=True)
	sorten_output = sorten_schema.dump(sorten_results)
	return simplejson.dumps(sorten_output, ensure_ascii=False, encoding='utf8'), 200


@app.route('/api/karte/baeume/<id>', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/id')
def get_tree(id):
	import schemas, models
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	tree_schema = schemas.Tree()
	tree_output = tree_schema.dump(tree_results)
	return simplejson.dumps(tree_output, ensure_ascii=False, encoding='utf8')


@app.route('/api/karte/baeume/koordinaten', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/koordinaten')
def get_coordinates():
	import schemas, models
	tree_results = DB.session.query(models.Pflanzliste).all()
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	schema = schemas.Treecoordinates(many=True)
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@app.route('/api/karte/baeume/<id>/koordinaten', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/<id>/koordinaten')
def get_coordinates_of_tree(id):
	import schemas, models
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	schema = schemas.Treecoordinates()
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@app.route('/api/karte/baeume/properties', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/properties')
def get_properties():
	import schemas, models
	sorten_results = DB.session.query(models.Sorten).all()
	print(sorten_results)
	if not sorten_results:
		return jsonify({'message': 'No tree found'}), 400
	schema = schemas.Sorten(many=True)
	output = schema.dump(sorten_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')
# join = DB.session.query(models.Pflanzliste, models.Sorten).join(models.Sorten).join(models.Pflanzliste)


# TODO
@app.route('/api/kontakt', methods=['POST'])
@cross_origin(origin='localhost:3000/kontakt')
def fetch_contact_information():
	firstname = request.form['Vorname']
	lastname = request.form['Nachname']
	street = request.form['Strasse']
	street_number = request.form['Nummer']
	postal_code = request.form['Postleitzahl']
	city = request.form['Ort']
	email = request.form['Email']
	message = request.form['Nachricht']


# TODO
@app.route('/api/login')
@cross_origin(origin='localhost:3000/login')
def login():
	return 'logger'
