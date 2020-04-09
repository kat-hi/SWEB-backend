import os
from oauthlib.oauth2 import WebApplicationClient


class Config:
	# DATABASE
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI_DEV']

	# SECRETS
	GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
	GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
	SESSION_SECRET_KEY = os.environ['SECRET_KEY']

	# LOGIN
	ADMIN_EMAIL_1 = os.environ['ADMIN_EMAIL_1']
	ADMIN_EMAIL_2 = os.environ['ADMIN_EMAIL_2']
	CLIENT = WebApplicationClient(GOOGLE_CLIENT_ID)
	GOOGLE_DISCOVERY_URL = os.environ['GOOGLE_DISCOVERY_URL']
	ADMIN_BASE_URL = os.environ['ADMIN_BASE_URL']

	# SMTP
	SMTP_PORT = os.environ['SMTP_PORT']
	SMTP_SERVER = os.environ['SMTP_SERVER']
	SENDER_EMAIL = os.environ['SENDER_EMAIL']
	RECEIVER_EMAIL = os.environ['RECEIVER_EMAIL']
	SMTP_PASSWORD = os.environ['SMTP_PASSWORD']

	IMAGE_BASE_URL = os.environ['IMAGE_BASE_URL']


class Production(Config):
	# DATABASE
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI_PROD']


