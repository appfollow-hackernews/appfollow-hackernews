import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appfollow_hackernews.settings')

if 'CLOUDAMQP_URL' in os.environ:  # pragma: no cover
    app = Celery('proj', broker=os.environ['CLOUDAMQP_URL'])
else:
    app = Celery('proj', broker='pyamqp://rabbitmq')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(['hackernews'])
