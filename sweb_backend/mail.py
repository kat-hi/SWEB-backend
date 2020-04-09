import smtplib, ssl
from _socket import gaierror
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sweb_backend.main import app

PORT = app.config['SMTP_PORT']
SERVER = app.config['SMTP_SERVER']
SENDER = app.config['SENDER_EMAIL']
RECEIVER = app.config['RECEIVER_EMAIL']
PASSWORD = app.config['SMTP_PASSWORD']


def _plain_text_mail(data):
	return 'Absender:\n' + data['firstname'] + ' ' + data['lastname'] + '\n' \
		+ data['streetAddress'] + '\n' + data['cityAddress'] + '\n' + data['email'] + '\n' \
		+ 'Tel: ' + data['phone'] + '\n\n' + 'Nachricht:\n' + data['message']


def connect_to_smtp_server(datalist):
	app.logger.info('LOGINTO: ' + str(datalist))
	message = MIMEMultipart("alternative")
	message["Subject"] = "Anfrage: Baumpatenschaft"
	message["From"] = RECEIVER
	message["To"] = RECEIVER
	part1 = MIMEText(_plain_text_mail(datalist), "plain")
	message.attach(part1)
	context = ssl.create_default_context()
	_send_email(context, message)


def _send_email(context, message):
	try:
		with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
			server.login(SENDER, PASSWORD)
			server.sendmail(SENDER, RECEIVER, message.as_string())
	except (gaierror, ConnectionRefusedError):
		app.logger.info('Failed to connect to the server. Bad connection settings?')
	except smtplib.SMTPServerDisconnected:
		app.logger.info('Failed to connect to the server. Wrong user/password?')
	except smtplib.SMTPException as e:
		app.logger.info('SMTP error occurred: ' + str(e))
	else:
		app.logger.info('Sent')
