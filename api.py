import simplejson
from flask import request, Blueprint
from flask_cors import cross_origin
from flask import jsonify
import json

api = Blueprint('api', __name__)


@api.route('/api', methods=['GET'])
@cross_origin()
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	return response


@api.route('/api/karte', methods=['GET'])
@cross_origin()
def infos():
	from main import DB, app
	import models, schemas

	tree_results = DB.session.query(models.Pflanzliste).all()
	tree_schema = schemas.Tree(many=True)
	trees_output = tree_schema.dump(tree_results)

	paten_results = DB.session.query(models.Paten).all()
	paten_schema = schemas.Paten(many=True)
	paten_output = paten_schema.dump(paten_results)

	for tree in trees_output:
		for pate in paten_output:
			app.logger.info('BAUMID: ' + str(tree['baumID']) + ' and PATENVALUES: ' + str(pate.values()))
			if str(tree["baumID"]) in pate.values():
				app.logger.info('BAUM IN PATE: ' + str(tree['baumID']))
				tree["pate"] = "true"
	return simplejson.dumps(trees_output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume', methods=['GET'])
@cross_origin()
def get_trees():
	from main import DB
	import models, schemas
	sorten_results = DB.session.query(models.Sorten).all()
	sorten_schema = schemas.Sorten(many=True)
	sorten_output = sorten_schema.dump(sorten_results)
	return simplejson.dumps(sorten_output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume/<id>', methods=['GET'])
@cross_origin()
def get_tree(id):
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	tree_schema = schemas.Tree()
	tree_output = tree_schema.dump(tree_results)
	return simplejson.dumps(tree_output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/koordinaten', methods=['GET'])
@cross_origin()
def get_coordinates():
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).all()
	schema = schemas.Treecoordinates(many=True)
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/<id>/koordinaten', methods=['GET'])
@cross_origin()
def get_coordinates_of_tree(id):
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	schema = schemas.Treecoordinates()
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/properties', methods=['GET'])
@cross_origin()
def get_properties():
	import schemas, models
	from main import DB
	sorten_results = DB.session.query(models.Sorten).all()
	schema = schemas.Sorten(many=True)
	output = schema.dump(sorten_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@api.route('/api/kontakt', methods=['POST'])
@cross_origin()
def fetch_contact_information():
	from mail import log_into_SMTP_Server_and_send_email
	response = json.loads(request.data.decode('utf-8'))
	email = response['email']
	lastname = response['lastName']
	address = response['address']
	message = response['message']
	firstname = response['firstName']
	log_into_SMTP_Server_and_send_email(firstname, lastname, email, address, message)
	return '', 200
