import os
from celery import Celery

# set default Django settings module for the 'celery' program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coursesity.settings")

app = Celery("coursesity")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
