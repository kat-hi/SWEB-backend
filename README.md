# Stark-Wie-Ein-Baum

["Stark wie ein Baum!“](https://www.hof-grueneberg.de/Stiftung/Stiftung-hof-grueneberg/#c1669) ist ein Gemeinschaftsprojekt des Caritas-Kinderhospizdienstes und der [Stiftung Hof Grüneberg](https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/).

https://app.stark-wie-ein-baum.de


**Projektpartner: Stiftung Hof Grüneberg**<br>
https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/

#### functionality
App
- Database-Api (mysql-db)
- Email-Transfer via smtp from form to client-email

Administration
- Authentication via OAuth2.0 (Google Login)
- Admin Interface to manipulate the database

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

### note
this repo is a copy of our private project.

frontend developer: wkrl (https://github.com/wkrl/Stark-Wie-Ein-Baum)

