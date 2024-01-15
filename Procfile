web: python3 manage.py migrate 
web: python3 manage.py collectstatic --noinput
web: gunicorn core.wsgi --log-file - 