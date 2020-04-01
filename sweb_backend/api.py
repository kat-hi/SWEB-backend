import simplejson
from flask import request, Blueprint
from flask import jsonify
import json
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
api = Blueprint('api', __name__)
from main import app

limiter = Limiter(
    app,
    key_func=get_remote_address,
	default_limits=['50 per day']
)

@api.route('/api', methods=['GET'])
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	return response


@api.route('/api/karte', methods=['GET'])
@limiter.exempt
def infos():
	from main import DB
	import models, schemas

	tree_results = DB.session.query(models.Pflanzliste).all()
	tree_schema = schemas.Tree(many=True)
	trees_output = tree_schema.dump(tree_results)

	return simplejson.dumps(trees_output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume', methods=['GET'])
@limiter.exempt
def get_trees():
	from main import DB
	import models, schemas
	sorten_results = DB.session.query(models.Sorten).all()
	sorten_schema = schemas.Sorten(many=True)
	sorten_output = sorten_schema.dump(sorten_results)
	return simplejson.dumps(sorten_output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume/<id>', methods=['GET'])
@limiter.exempt
def get_tree(id):
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	tree_schema = schemas.Tree()
	tree_output = tree_schema.dump(tree_results)
	return simplejson.dumps(tree_output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates():
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).all()
	schema = schemas.Treecoordinates(many=True)
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/<id>/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates_of_tree(id):
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	schema = schemas.Treecoordinates()
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/properties', methods=['GET'])
@limiter.exempt
def get_imagelinks():
	import schemas, models
	from main import DB
	from config import Config
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
	return jsonify({'data': checked_files})


@api.route('/api/kontakt', methods=['POST'])
def fetch_contact_information():
	from mail import log_into_SMTP_Server_and_send_email
	response = json.loads(request.data.decode('utf-8'))
	email = str(response['email'])
	lastname = str(response['lastName'])
	streetaddress = str(response['streetAddress'])
	cityaddress = str(response['cityAddress'])
	message = str(response['message'])
	firstname = str(response['firstName'])
	phone = str(response['phone'])
	app.logger.info('API INFO: ' + email + ' ' + lastname+ ' ' + firstname + ' ' + cityaddress + ' ' + streetaddress+ ' ' + message + ' ' + phone)
	log_into_SMTP_Server_and_send_email(firstname, lastname, email, phone, streetaddress, cityaddress, message)
	return '', 200
