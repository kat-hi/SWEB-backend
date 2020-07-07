# Stark-Wie-Ein-Baum

["Stark wie ein Baum!“](https://www.hof-grueneberg.de/Stiftung/Stiftung-hof-grueneberg/#c1669) ist ein Gemeinschaftsprojekt des Caritas-Kinderhospizdienstes und der [Stiftung Hof Grüneberg](https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/).

https://app.stark-wie-ein-baum.de


**Projektpartner: Stiftung Hof Grüneberg**<br>
https://www.hof-grueneberg.de/stiftung/stiftung-hof-grueneberg/

#### functionality
App
- Database-Api (mysql-db)
- smtp

Administration
- Authentication via OAuth2.0 (Google Login)
- Admin Interface to manipulate the database

### docker-compose
cd SWEB-backend
```
sudo docker-compose build
sudo docker-compose up
```


## docker
cd SWEB_backend/sweb_backend

```
docker build -t <registryname>/<namespace>/sweb_backend:<tag> -f ../Dockerfile .
docker push <registryname>/<namespace>/sweb:backend:<tag>
```

## starting in dev mode with virtualenv + local mysqldb
unix:

```
cd api
source venv/bin/activate
source .env
export FLASK_ENV=dev
flask run
```

### note
this repo is a copy of our private project.

frontend developer: wkrl (https://github.com/wkrl/Stark-Wie-Ein-Baum)


### current domains

swebapi.demo.datexis.com (api baseurl used by frontend)

swebapi.dev.demo.datexis.com (development: test and approve new changes)

swebapi.monitoring.demo.datexis.com (monitoring app that sends an email if /api/karte does not return <200>)


admin.stark-wie-ein-baum.de (accessing the admin portal)

app.stark-wie-ein-baum.de (accessing sweb frontend)
