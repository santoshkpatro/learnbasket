# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techowiz.settings.development')

# app = Celery('techowiz', broker='redis://localhost', backend='redis://localhost')
# # app.autodiscover_tasks()
# # app.config_from_object('django.conf:settings', namespace='CELERY')

# @app.task
# def mul(x ,y):
#     return x * y
