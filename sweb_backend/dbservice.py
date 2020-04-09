from sweb_backend import schemas, models
import simplejson
from sweb_backend.main import DB


class DB_SERVICE:
	def _get_model_obj(self, model, id):
		if id is None:
			return DB.session.query(model)
		else:
			return DB.session.query(model).get(id)

	def _get_schema_obj(self, schema, id):
		if id is None:
			return schema(many=True)
		else:
			return schema()

	def get_json_data(self, model, schema, id):
		output = self._get_schema_obj(schema, id).dump(self._get_model_obj(model, id))
		return simplejson.dumps(output, ensure_ascii=False, encoding='utf8'), 200
