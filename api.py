import simplejson
from flask import request, Blueprint
from flask_cors import cross_origin
from flask import jsonify

api = Blueprint('api', __name__)

@api.route('/api', methods=['GET'])
@cross_origin(origin='localhost:3000/')
def index():
	response = jsonify({'json sagt': 'Hallo i bims. der json.'})
	return response


@api.route('/api/karte', methods=['GET'])
@cross_origin(origin='localhost:3000/karte')
def infos():
	from main import DB
	import models, schemas
	tree_results = DB.session.query(models.Pflanzliste).all()
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	tree_schema = schemas.Tree(many=True)
	trees_output = tree_schema.dump(tree_results)
	return simplejson.dumps(trees_output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume')
def get_trees():
	from main import DB
	import models, schemas
	sorten_results = DB.session.query(models.Sorten).all()
	if not sorten_results:
		return jsonify({'message': 'No entry found'}), 400
	sorten_schema = schemas.Sorten(many=True)
	sorten_output = sorten_schema.dump(sorten_results)
	return simplejson.dumps(sorten_output, ensure_ascii=False, encoding='utf8'), 200


@api.route('/api/karte/baeume/<id>', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/id')
def get_tree(id):
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	tree_schema = schemas.Tree()
	tree_output = tree_schema.dump(tree_results)
	return simplejson.dumps(tree_output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/koordinaten', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/koordinaten')
def get_coordinates():
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).all()
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	schema = schemas.Treecoordinates(many=True)
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/<id>/koordinaten', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/<id>/koordinaten')
def get_coordinates_of_tree(id):
	import schemas, models
	from main import DB
	tree_results = DB.session.query(models.Pflanzliste).get(id)
	if not tree_results:
		return jsonify({'message': 'No tree found'}), 400
	schema = schemas.Treecoordinates()
	output = schema.dump(tree_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')


@api.route('/api/karte/baeume/properties', methods=['GET'])
@cross_origin(origin='localhost:3000/karte/baeume/properties')
def get_properties():
	import schemas, models
	from main import DB
	sorten_results = DB.session.query(models.Sorten).all()
	print(sorten_results)
	if not sorten_results:
		return jsonify({'message': 'No tree found'}), 400
	schema = schemas.Sorten(many=True)
	output = schema.dump(sorten_results)
	return simplejson.dumps(output, ensure_ascii=False, encoding='utf8')
	# join = DB.session.query(models.Pflanzliste, models.Sorten).join(models.Sorten).join(models.Pflanzliste)

# TODO
@api.route('/api/kontakt', methods=['POST'])
@cross_origin(origin='localhost:3000/kontakt')
def fetch_contact_information():
	from main import DB

	firstname = request.form['Vorname']
	lastname = request.form['Nachname']
	street = request.form['Strasse']
	street_number = request.form['Nummer']
	postal_code = request.form['Postleitzahl']
	city = request.form['Ort']
	email = request.form['Email']
	message = request.form['Nachricht']
