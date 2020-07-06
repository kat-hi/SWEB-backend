import smtplib, ssl
from _socket import gaierror
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .main import app
from .config import Config

PORT = Config.SMTP['PORT']
SERVER = Config.SMTP['SERVER']
SENDER = Config.SMTP['SENDER']
RECEIVER = Config.SMTP['RECEIVER']
PASSWORD = Config.SMTP['PASSWORD']


def _plain_text_mail(data):
	return 'Absender:\n' + data['firstName'] + ' ' + data['lastName'] + '\n' \
		+ data['streetAddress'] + '\n' + data['cityAddress'] + '\n' + data['email'] + '\n' \
		+ 'Tel: ' + data['phone'] + '\n\n' + 'Nachricht:\n' + data['message']


def connect_to_smtp_server(datalist):
	app.logger.info('LOGINTO: ' + str(datalist))
	message = MIMEMultipart("alternative")
	message["Subject"] = "Anfrage: Baumpatenschaft"
	message["From"] = datalist['email']
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
