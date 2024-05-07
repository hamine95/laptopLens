# celery.py

from __future__ import absolute_import, unicode_literals
import datetime
import os

from celery import Celery
from django.conf import settings
# from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptoplens.settings')

app = Celery('laptoplens')  # Replace 'your_project' with your project's name.

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "sample_task": {
        "task": "get_new_announcements",
        "schedule": 300,
    },
}