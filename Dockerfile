# server setup
FROM python:3.6

# install requirements
COPY sweb_backend /start/

WORKDIR start

RUN chmod +x /start/requirements.txt

RUN pip install -r /start/requirements.txt --no-cache-dir --compile

ENV FLASK_ENV="docker"

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["flask", "run", "--host","0.0.0.0"]