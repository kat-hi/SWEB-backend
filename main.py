import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import simplejson
from flask_admin import Admin
from flask_cors import CORS, cross_origin
import os
from flask import Flask, redirect, request, url_for
from flask_login import (
	LoginManager,
	current_user,
	login_required,
	login_user,
	logout_user,
)
from werkzeug import serving
import ssl
import requests

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
	app.secret_key = Config.SECRETS['SECRET_KEY']


def create_tables():
	app.app_context().push()
	import models
	from admin import pflanzlistetable, obstsortentable, patentable
	admin.add_view(pflanzlistetable(models.Pflanzliste, DB.session))
	admin.add_view(obstsortentable(models.Sorten, DB.session))
	admin.add_view(patentable(models.Paten, DB.session))


def get_google_provider_cfg():
	return requests.get(Config.GOOGLE_DISCOVERY_URL).json()


app = create_app()
app.app_context().push()
from config import Config, Production
set_environment()
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


@app.route('/api/admin')
def admin_home():
	if current_user.is_authenticated:
		return "<p>Du bist eingeloggt!</p>"
	else:
		return '<a class="button" href="/api/admin/login">Google Login</a>'


@app.route('/api/admin/login')
def login():
	# Find out what URL to hit for Google login
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]

	# Use library to construct the request for Google login and provide
	# scopes that let you retrieve user's profile from Google
	request_uri = Config.CLIENT.prepare_request_uri(
		authorization_endpoint,
		redirect_uri=request.base_url + "/callback",
		scope=["openid", "email", "profile"],
	)
	print(request_uri)
	return redirect(request_uri)

@app.route("/api/admin/logout")
@login_required
def logout():
	return "<p>Du bist ausgeloggt!</p>"


@app.route("/api/admin/login/callback")
def callback():
	# Get authorization code Google sent back to you
	code = request.args.get("code")
	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]
	token_url, headers, body = Config.CLIENT.prepare_token_request(
		token_endpoint,
		authorization_response=request.url,
		redirect_url=request.base_url,
		code=code
	)
	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(Config.SECRETS['GOOGLE_CLIENT_ID'], Config.SECRETS['GOOGLE_CLIENT_SECRET'])
	)
	Config.CLIENT.parse_request_body_response(json.dumps(token_response.json()))
	# Now that you have tokens (yay) let's find and hit the URL
	# from Google that gives you the user's profile information,
	# including their Google profile image and email
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	uri, headers, body = Config.CLIENT.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)
	# You want to make sure their email is verified.
	# The user authenticated with Google, authorized your
	# app, and now you've verified their email through Google!
	if userinfo_response.json().get("email_verified"):
		unique_id = userinfo_response.json()["sub"]
		users_email = userinfo_response.json()["email"]
		picture = userinfo_response.json()["picture"]
		users_name = userinfo_response.json()["given_name"]
	else:
		return "User email not available or not verified by Google.", 400
	from admin_user import User
	user = User(
		id_=unique_id, name=users_name, email=users_email, profile_pic=picture
	)
	login_user(user)
