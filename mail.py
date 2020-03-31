import smtplib, ssl
from _socket import gaierror
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

PORT = Config.SMTP['PORT']
SERVER = Config.SMTP['SERVER']
SENDER = Config.SMTP['SENDER']
RECEIVER = Config.SMTP['RECEIVER']
PASSWORD = Config.SMTP['PASSWORD']
from main import app


def plain_text_mail(firstname, lastname, email, phone, streetaddress, cityaddress, user_message):
	app.logger.info('PLAINTEXT: ' + firstname + ' ' + lastname + ' ' + email+ ' ' + phone + ' ' + streetaddress + ' ' + cityaddress+ ' ' + user_message)
	return 'Absender:\n' + firstname + ' ' + lastname + '\n' + streetaddress + '\n' + cityaddress + '\n' + email + '\n' + 'Tel: ' + phone + '\n\n' + 'Nachricht:\n' + user_message


def log_into_SMTP_Server_and_send_email(firstname, lastname, email, phone, streetaddress, cityaddress, user_message):
	app.logger.info('LOGINTO: ' + firstname + ' ' + lastname + ' ' + email + ' ' + phone + ' ' + streetaddress + ' ' +cityaddress+ ' ' +user_message)

	message = MIMEMultipart("alternative")
	message["Subject"] = "Anfrage: Baumpatenschaft"
	message["From"] = RECEIVER
	message["To"] = RECEIVER
	part1 = MIMEText(plain_text_mail(firstname, lastname, email, phone, cityaddress, streetaddress, user_message), "plain")
	message.attach(part1)
	app.logger.info(str(part1))
	context = ssl.create_default_context()

	try:
		with smtplib.SMTP_SSL(SERVER, PORT, context=context) as server:
			server.login(SENDER, PASSWORD)
			server.sendmail(SENDER, RECEIVER, message.as_string())
	except (gaierror, ConnectionRefusedError):
		print('Failed to connect to the server. Bad connection settings?')
	except smtplib.SMTPServerDisconnected:
		print('Failed to connect to the server. Wrong user/password?')
	except smtplib.SMTPException as e:
		print('SMTP error occurred: ' + str(e))
	else:
		print('Sent')
