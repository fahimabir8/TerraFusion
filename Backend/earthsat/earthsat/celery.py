# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'satellite_tracker.settings')

# app = Celery('satellite_tracker')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'earthsat.settings')

app = Celery('earthsat')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps
app.autodiscover_tasks()
