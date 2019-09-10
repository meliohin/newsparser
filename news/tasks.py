from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import News

@shared_task
def regular_task():
    News.process()