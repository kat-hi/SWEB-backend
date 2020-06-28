# server setup
FROM python:3.6

# install requirements
COPY . sweb_backend/

WORKDIR sweb_backend

RUN chmod +x requirements.txt

RUN pip install -r requirements.txt --no-cache-dir --compile

ENV FLASK_ENV="production"

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["flask", "run", "--host","0.0.0.0"]
