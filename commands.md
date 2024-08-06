## start a worker:
    - celery -A <appname> worker -l info

## start flower:
    - celery -A <appname> flower

## start rabbitmq
    - docker run -it --rm --name rabbitmq -p 56772:5672 -p 15672:15672 rabbitmq:3.13.1-management
## start django server for SSL/TLS cert
    - python manage.py runserver_plus --cert-file cert.crt