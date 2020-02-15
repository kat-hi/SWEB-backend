from flask_login import (current_user, login_required, login_user, logout_user)
import requests
from config import Config
from flask import request, redirect, Blueprint
import json

admin_login = Blueprint('admin_login', __name__)

from main import login_manager

users_email = ""

# TODO HttpError handling
# getting the provider configuration document
def get_google_provider_cfg():
	return requests.get(Config.GOOGLE_DISCOVERY_URL).json()


@login_manager.user_loader
def user_loader(id):
	from models import Admin
	from main import DB,app
	global users_email
	app.logger.info('USER LOADER, SHOW EMAIL: ' + str(id))
	user = Admin.query.get(users_email)
	# user = DB.session.query(Admin).get(users_email)
	app.logger.info('USER LOADER; PRINT DATABASE QUERY: ' + str(user))
	return user


@login_manager.user_loader
def load_user(id):
	global users_email
	from models import Admin
	from main import DB, app
	app.logger.info('LOAD USER, SHOW ID: ' + str(id))
	app.logger.info('LOAD USER, SHOW EMAIL: ' + str(id))
	user = DB.session.query(Admin).get(users_email)
	app.logger.info('LOAD USER; PRINT DATABASE QUERY: ' + str(user))
	return user


def flask_user_authentication(users_email):
	from models import Admin
	from main import DB, app
	if users_email == Config.ADMIN_EMAIL:
		app.logger.info('FLASK USER AUTH; USER_EMAIL EQUALS ADMIN_EMAIL')
		admin = DB.session.query(Admin).get(users_email)
		admin.authenticated = "true"
		admin.active = "true"
		DB.session.add(admin)
		DB.session.commit()
		login_user(admin, remember=True)
		return True
	else:
		app.logger.info('FLASK USER AUTHENTICATION FAILED')
		return False


@admin_login.route('/api/admin')
def admin_home():
	from main import app
	if current_user.is_authenticated:
		app.logger.info('current user: ' + str(current_user))
		return "<p>Du bist eingeloggt!</p>"
	else:
		app.logger.info('ADMIN HOME: USER NEEDS TO AUTHENTICATE FIRST')
		return '<a class="button" href="/api/admin/login">Google Login</a>'


@admin_login.route('/api/admin/login')
def google_login():
	from main import app
	app.logger.info('request /api/admin/login')
	# auth-endpoint contains URL to instantiate the OAuth2 flow with Google from this client app
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]
	app.logger.info('got auth-endpoint: ' + authorization_endpoint)
	# Use library to construct request for Google login + provide scopes that let retrieve user's profile from Google
	request_uri = Config.CLIENT.prepare_request_uri(
		authorization_endpoint,
		redirect_uri=request.base_url.replace('http://', 'https://') + "/callback",
		scope=["openid", "email", "profile"])
	app.logger.info('Got request uri: ' + request_uri)
	return redirect(request_uri)


@admin_login.route("/api/admin/login/callback")
def callback():
	global users_email
	from main import app
	# Get authorization code Google sent back to you
	code = request.args.get("code")
	app.logger.info('got code from /callback ' + code)
	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]
	app.logger.info('GOT TOKEN_ENDPOINT from /callback ' + token_endpoint)
	token_url, headers, body = Config.CLIENT.prepare_token_request(
		token_endpoint,
		authorization_response=request.url.replace('http://', 'https://'),
		redirect_url=request.base_url.replace('http://', 'https://'),
		code=code)
	app.logger.info('GOT TOKEN_URL from /callback ' + token_url)
	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(Config.SECRETS['GOOGLE_CLIENT_ID'], Config.SECRETS['GOOGLE_CLIENT_SECRET']))

	app.logger.info('GOT TOKEN RESPONSE from /callback ' + str(token_response))
	Config.CLIENT.parse_request_body_response(json.dumps(token_response.json()))
	# find and hit the URL from Google that gives you the user's profile information,
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	app.logger.info('GOT USERINFO_ENDPOINT from /callback ' + userinfo_endpoint)
	uri, headers, body = Config.CLIENT.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)
	app.logger.info('GOT USERINFO_RESPONSE from /callback ' + str(userinfo_response))

	# verification
	# if userinfo_response.json().get("email_verified"):
	unique_id = userinfo_response.json()["sub"]
	users_email = userinfo_response.json()["email"]
	users_name = userinfo_response.json()["given_name"]
	app.logger.info('GOT USER DATA from /callback: ' + unique_id + ' ' + users_email + ' ' + users_name)
	app.logger.info('CURRENT USER: ' + str(current_user))
	app.logger.info('ADMIN EMAIL: ' + str(Config.ADMIN_EMAIL) + ' and user mail: ' + str(users_email))

	if flask_user_authentication(users_email):
		return redirect('https://demo.datexis.com/admin')
	else:
		return "Sorry. You're Email is not valid.", 400


@admin_login.route("/test")
@login_required
def get_user_data():
	from main import app
	app.logger.info('GET USER DATA; CURRENT USER: ' + str(current_user))
	return '<a class="button" href="/api/admin/logout">Logout</a>'


@admin_login.route("/logout")
@login_required
def logout():
	from main import DB, app
	app.logger.info('logout')
	admin = current_user
	admin.authenticated = False
	DB.session.add(admin)
	DB.session.commit()
	logout_user()
	return redirect('https://demo.datexis.com/api/admin')
