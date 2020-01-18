# Backend configuration

## Docker

* Build image: `docker build .`.
* Migrate database: `docker-compose run web python /code/manage.py migrate --noinput`.
* Create superuser: `docker-compose run web python /code/manage.py createsuperuser`.
* Run docker: `docker-compose up -d --build`.
* Close docker container: `ocker-compose down`.

## Resources

* [How to use Django, PostgreSQL, and Docker - William Vincent](https://wsvincent.com/django-docker-postgresql/)
* [Deploying Django to Heroku With Docker | TestDriven.io](https://testdriven.io/blog/deploying-django-to-heroku-with-docker/)
