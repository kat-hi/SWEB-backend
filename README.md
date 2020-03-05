# Stark-Wie-Ein-Baum

### URL zur App
https://app.stark-wie-ein-baum.de


**Projektpartner: Stiftung Hof Grüneberg**<br>
https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/


### docker-compose
```
sudo docker-compose build
sudo docker-compose up
```

## starting in dev mode with virtualenv
on linux

```
cd api
source venv/bin/activate
source .env
export FLASK_ENV=dev
flask run
```

The flask-server runs on http://127.0.0.1:5000

