import os
from celery import Celery

# set default Django settings module for the 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursesity.settings")

app = Celery("coursesity")
app.config_from_object("django.conf:settings", namespace="CELERY")
broker_url = os.getenv("RABBITMQ_BROKER_URL", "amqp://guest:guest@localhost:5672//")

app.conf.broker_url = broker_url

app.autodiscover_tasks()
