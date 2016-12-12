"""
WSGI config for MAT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

root_path = '/home/caleb/www/'
sys.path.insert(0, '/home/caleb/anaconda2/envs/MARS/lib/python2.7/site-packages/')
sys.path.insert(0, '/home/caleb/www/MARS/')
sys.path.insert(0, '/home/caleb/www/MARS/MAT/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'MAT.settings'


application = get_wsgi_application()

