#from __future__ import absolute_import

#import os

#from celery import Celery
import requests
# set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MAT.settings')

from django.conf import settings

#app = Celery('MAT')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
#app.config_from_object('django.conf:settings')
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
#
# @app.task
# def fetch_url(url):
#     resp = requests.get(url)
#     print resp.status_code
#
#
# def func(urls):
#     for url in urls:
#         fetch_url.delay(url)
#
# if __name__ == "__main__":
#     func(["http://google.com", "https://amazon.in", "https://facebook.com", "https://twitter.com", "https://alexa.com"])