# Stark-Wie-Ein-Baum

**Homepage Hof Grüneberg**<br>
https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/

### server
## starting in production mode
```
sudo docker-compose build
sudo docker-compose up
```

## starting in dev mode

on linux
```
cd api
export FLASK_ENV=dev
source venv/bin/activate
source .env
flask run
```

The flask-server runs on http://127.0.0.1:5000

### frontend

```
yarn start
```

Frontend runs on https://127.0.0.1:3000
