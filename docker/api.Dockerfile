# server setup
FROM python:3.6

# install requirements
COPY . /start/

WORKDIR start

RUN chmod +x /start/requirements.txt

RUN pip install -r /start/requirements.txt --no-cache-dir --compile

ENV FLASK_ENV="docker"

EXPOSE 5000

CMD ["flask", "run", "--host","0.0.0.0"]
