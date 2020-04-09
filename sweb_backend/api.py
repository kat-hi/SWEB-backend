from flask import request, Blueprint
from flask import jsonify
import json
import requests
import re

from sweb_backend.main import limiter
from sweb_backend.dbservice import DB_SERVICE
from sweb_backend import models,schemas
api = Blueprint('api', __name__)
db_service = DB_SERVICE()


@api.route('/api', methods=['GET'])
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	return response, 200


@api.route('/api/karte', methods=['GET'])
@limiter.exempt
def infos():
	return db_service.get_json_data(models.Plantlist, schemas.Tree, id=None)


@api.route('/api/karte/baeume', methods=['GET'])
@limiter.exempt
def get_trees():
	return db_service.get_json_data(models.Sorts, schemas.Sorts, id=None)


@api.route('/api/karte/baeume/<id>', methods=['GET'])
@limiter.exempt
def get_tree(id):
	return db_service.get_json_data(models.Plantlist, schemas.Tree, id=id)


@api.route('/api/karte/baeume/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates():
	return db_service.get_json_data(models.Plantlist, schemas.Treecoordinates, id=None)


@api.route('/api/karte/baeume/<id>/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates_of_tree(id):
	return db_service.get_json_data(models.Plantlist, schemas.Treecoordinates, id=id)


#TODO Refactoring
@api.route('/api/karte/baeume/properties', methods=['GET'])
@limiter.exempt
def get_imagelinks():
	from sweb_backend.main import app
	image_output = db_service.get_json_data(models.Image, schemas.Image, id=None)
	checked_files = []
	base_download_url = app.config['IMAGE_BASE_URL']
	for image in image_output:
		regex='lnk/[\w]*'
		image_id = re.search(regex, image['uri']).group().split('lnk/')[1]
		response = requests.head(base_download_url+image_id)
		if response.status_code is 200 and (response.headers['Content-Type'] == 'image/png' or response.headers['Content-Type'] == 'image/jpeg'):
			app.logger.info(str(response))
			checked_files.append(base_download_url+image_id)
	return jsonify({'data': checked_files}), 200


@api.route('/api/kontakt', methods=['POST'])
@limiter.limit('10 per hour', override_defaults=False)
def fetch_contact_information():
	from sweb_backend.mail import log_into_SMTP_Server_and_send_email
	from sweb_backend.main import app
	response = json.loads(request.data.decode('utf-8'))
	email = str(response['email'])
	lastname = str(response['lastName'])
	streetaddress = str(response['streetAddress'])
	cityaddress = str(response['cityAddress'])
	message = str(response['message'])
	firstname = str(response['firstName'])
	phone = str(response['phone'])
	app.logger.info('MAIL API INFO: ' + email + ' ' + lastname + ' ' + firstname + ' ' + cityaddress + ' ' + streetaddress + ' ' + message + ' ' + phone)
	log_into_SMTP_Server_and_send_email(firstname, lastname, email, phone, streetaddress, cityaddress, message)
	return '', 200

