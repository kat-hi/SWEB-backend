import simplejson
from flask import request, Blueprint
from flask import jsonify
import json
import requests
import re

api = Blueprint('api', __name__)
from sweb_backend.main import limiter


@api.route('/api', methods=['GET'])
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	return response, 200


@api.route('/api/karte', methods=['GET'])
@limiter.exempt
def infos():
	from sweb_backend import models, schemas
	from sweb_backend.main import DB
	tree_results = DB.session.query(models.Pflanzliste).all()
	tree_schema = schemas.Tree(many=True)
	trees_output = tree_schema.dump(tree_results)
	return simplejson.dumps(trees_output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume', methods=['GET'])
@limiter.exempt
def get_trees():
	from sweb_backend import models, schemas
	from sweb_backend.main import DB
	sorten_results = DB.session.query(models.Sorten).all()
	sorten_schema = schemas.Sorten(many=True)
	sorten_output = sorten_schema.dump(sorten_results)
	return simplejson.dumps(sorten_output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume/<id>', methods=['GET'])
@limiter.exempt
def get_tree(id):
	from sweb_backend import schemas, models
	from sweb_backend.main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	tree_schema = schemas.Tree()
	tree_output = tree_schema.dump(tree_results)
	return simplejson.dumps(tree_output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates():
	from sweb_backend import schemas, models
	from sweb_backend.main import DB
	tree_results = DB.session.query(models.Pflanzliste).all()
	schema = schemas.Treecoordinates(many=True)
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume/<id>/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates_of_tree(id):
	from sweb_backend import schemas, models
	from sweb_backend.main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	schema = schemas.Treecoordinates()
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume/properties', methods=['GET'])
@limiter.exempt
def get_imagelinks():
	from sweb_backend import schemas, models
	from sweb_backend.config import Config
	from sweb_backend.main import DB, app
	image_results = DB.session.query(models.Image).all()
	image_schema = schemas.Image(many=True)
	image_output = image_schema.dump(image_results)
	app.logger.info(str(image_output))

	checked_files = []
	base_download_url = Config.IMAGE_BASE_URL
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

