web: python3 manage.py migrate 
web: python3 manage.py collectstatic --noinput
web: gunicorn testForFundamental.wsgi --log-file - 