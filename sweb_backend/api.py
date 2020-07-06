from flask import request, Blueprint
from flask import jsonify
import json
from .main import limiter
from . import dataservice, dbservice
from . import models, schemas

api = Blueprint('api', __name__)


@api.route('/api', methods=['GET'])
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	return response, 200


@api.route('/api/karte', methods=['GET'])
@limiter.exempt
def infos():
	return dbservice.get_json_data(models.Plantlist, schemas.Tree, id=None)


@api.route('/api/karte/baeume', methods=['GET'])
@limiter.exempt
def get_trees():
	return dbservice.get_json_data(models.Sorts, schemas.Sorts, id=None)


@api.route('/api/karte/baeume/<id>', methods=['GET'])
@limiter.exempt
def get_tree(id):
	return dbservice.get_json_data(models.Plantlist, schemas.Tree, id=id)


@api.route('/api/karte/baeume/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates():
	return dbservice.get_json_data(models.Plantlist, schemas.Treecoordinates, id=None)


@api.route('/api/karte/baeume/<id>/koordinaten', methods=['GET'])
@limiter.exempt
def get_coordinates_of_tree(id):
	return dbservice.get_json_data(models.Plantlist, schemas.Treecoordinates, id=id)


@api.route('/api/karte/baeume/properties', methods=['GET'])
@limiter.exempt
def get_imagelinks():
	image_output = dbservice.get_json_data(models.Image, schemas.Image, id=None)
	checked_files = dataservice.get_valid_image_uri(image_output)
	return jsonify({'data': checked_files}), 200


@api.route('/api/kontakt', methods=['POST'])
@limiter.limit('10 per hour', override_defaults=False)
def fetch_contact_information():
	from .mail import connect_to_smtp_server
	response = json.loads(request.data.decode('utf-8'))
	connect_to_smtp_server(response)
	return '', 200
