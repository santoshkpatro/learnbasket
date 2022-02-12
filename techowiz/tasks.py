# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techowiz.settings.development')

# app = Celery('techowiz', broker='redis://localhost', backend='redis://localhost')

# @app.task
# def add(x, y):
#     return x + y