web: gunicorn app.wsgi
release: python manage.py makemigrations --noinput
heroku config:set DISABLE_COLLECTSTATIC=1
release: python manage.py migrate --noinput