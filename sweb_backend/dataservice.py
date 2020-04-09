import requests
import re
from sweb_backend.main import app


def extract_values_from_json(response):
	email = str(response['email'])
	lastname = str(response['lastName'])
	streetaddress = str(response['streetAddress'])
	cityaddress = str(response['cityAddress'])
	message = str(response['message'])
	firstname = str(response['firstName'])
	phone = str(response['phone'])
	data = [email, lastname, streetaddress, cityaddress, message, firstname, phone]
	app.logger.info('extract_values_from_json: ' + str(data))
	return data


def get_valid_image_uri(image_output):
	checked_files = []
	base_download_url = app.config['IMAGE_BASE_URL']
	for image in image_output:
		regex = 'lnk/[\w]*'
		image_id = re.search(regex, image['uri']).group().split('lnk/')[1]
		response = requests.head(base_download_url + image_id)
		if response.status_code is 200 and (
			response.headers['Content-Type'] == 'image/png' or response.headers['Content-Type'] == 'image/jpeg'):
			app.logger.info('get_valid_image_uri ' + str(response))
			checked_files.append(base_download_url + image_id)
	return checked_files
