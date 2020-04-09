from flask_login import (current_user, login_required, login_user, logout_user)
import requests
from flask import request, redirect, Blueprint, render_template
import json

admin_login = Blueprint('admin_login', __name__)
from sweb_backend.config import Config
from sweb_backend.main import login_manager, app

USERS_EMAIL = ""
ADMIN_BASE_URL = app.config['ADMIN_BASE_URL']


# TODO HttpError handling
# getting the provider configuration document
def get_google_provider_cfg():
	return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()


# this function is to associate the user_id in the cookie with the actual user object
# user_id is the user_id from the cookies that is created when a user logs in.
@login_manager.user_loader
def load_user(user_id):
	global USERS_EMAIL
	from sweb_backend.models import Admins
	from sweb_backend.main import DB, app
	app.logger.info('LOAD USER, SHOW EMAIL: ' + str(user_id))
	user = DB.session.query(Admins).get(USERS_EMAIL)
	return user


def flask_user_authentication(users_email):
	from sweb_backend.models import Admins
	from sweb_backend.main import DB, app
	if users_email == app.config['ADMIN_EMAIL_1'] or users_email == app.config['ADMIN_EMAIL_2']:
		admin = DB.session.query(Admins).get(users_email)
		admin.authenticated = 'true'
		admin.active = 'true'
		DB.session.add(admin)
		DB.session.commit()
		login_user(admin, remember=True)
		return True
	else:
		app.logger.info('FLASK USER AUTHENTICATION FAILED')
		return False


@admin_login.route('/')
def root():
	if str(request.url) == 'http://' + ADMIN_BASE_URL or str(request.url) == 'https://' + ADMIN_BASE_URL:
		return redirect('https://' + ADMIN_BASE_URL + 'app/admin')
	else:
		pass


@admin_login.route('/app/admin')
def admin_home():
	from sweb_backend.main import app
	if current_user.is_authenticated:
		app.logger.info('current user: ' + str(current_user))
		return redirect('https://' + ADMIN_BASE_URL + 'admin')
	else:
		return render_template('login.html')


@admin_login.route('/app/admin/login')
def google_login():
	# auth-endpoint contains URL to instantiate the OAuth2 flow with Google from this client app
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg['authorization_endpoint']
	# Use library to construct request for Google login + provide scopes that let retrieve user's profile from Google
	request_uri = app.config['CLIENT'].prepare_request_uri(
		authorization_endpoint,
		redirect_uri=request.base_url.replace('http://', 'https://') + '/callback',
		scope=['openid', 'email', 'profile'])
	return redirect(request_uri)


@admin_login.route("/app/admin/login/callback")
def callback():
	global USERS_EMAIL
	from sweb_backend.main import app
	# Get authorization code Google sent back to you
	code = request.args.get("code")
	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]
	token_url, headers, body = app.config['CLIENT'].prepare_token_request(
		token_endpoint,
		authorization_response=request.url.replace('http://', 'https://'),
		redirect_url=request.base_url.replace('http://', 'https://'),
		code=code
	)
	app.logger.info('GOT TOKEN_URL from /callback ' + token_url)
	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET'])
	)

	app.config['CLIENT'].parse_request_body_response(json.dumps(token_response.json()))
	# find and hit the URL from Google that gives you the user's profile information,
	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	uri, headers, body = app.config['CLIENT'].add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)

	# verification
	# if userinfo_response.json().get("email_verified"):
	unique_id = userinfo_response.json()["sub"]
	USERS_EMAIL = userinfo_response.json()["email"]
	users_name = userinfo_response.json()["given_name"]
	app.logger.info('GOT USER DATA from /callback: ' + unique_id + ' ' + USERS_EMAIL + ' ' + users_name)

	if flask_user_authentication(USERS_EMAIL):
		return redirect('https://' + ADMIN_BASE_URL + 'admin')
	else:
		return "Sorry. Your email is not valid.", 400


@admin_login.route("/app/admin/logout")
@login_required
def logout():
	from sweb_backend.main import DB, app
	app.logger.info('logout')
	admin = current_user
	admin.authenticated = False
	DB.session.add(admin)
	DB.session.commit()
	logout_user()
	return redirect('https://' + ADMIN_BASE_URL + 'app/admin')
