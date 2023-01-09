from __future__ import unicode_literals,absolute_import
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Poll.settings')

app = Celery('Poll')


BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_BROKER_URL = os.environ.get('REDIS_URL')
app.conf.broker_url = BASE_REDIS_URL



app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'deactivate-24-hour':{
        'task':'user.tasks.deactivate_poll',
        'schedule':60,
      
    }
}
