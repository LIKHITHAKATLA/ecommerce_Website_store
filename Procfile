web: gunicorn ecommerce_Website.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn ecommerce_Website.wsgi