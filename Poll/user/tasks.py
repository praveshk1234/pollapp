
from django.utils import timezone
from celery.schedules import crontab

from celery import shared_task
from .models import Poll

@shared_task()
def deactivate_poll():
    
    files = Poll.objects.filter(publishedAt__lte=timezone.now())
    if files:
        files.delete()
        return "poll deactivate"
    else:
        return "no active polls" 