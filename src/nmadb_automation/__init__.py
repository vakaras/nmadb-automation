#!/usr/bin/python

'''
Monkey patch for celery.

Add this to settings.py:

    import djcelery
    djcelery.setup_loader()
    BROKER_URL = 'django://'

    INSTALLED_APPS += (
        'nmadb_automation',
        'djcelery',
        'kombu.transport.django',
        )
'''

import os
import billiard.forking
from django.conf import settings

BIN_DIR = os.path.join(settings.BUILDOUT_DIR, 'bin')


old_get_command_line = billiard.forking.get_command_line
def wrapper_get_command_line():
    rez = old_get_command_line()
    import sys
    rez = [sys.executable,
           os.path.join(BIN_DIR, 'billiard'),
           '--billiard-fork']
    return rez
billiard.forking.get_command_line = wrapper_get_command_line


old_get_preparation_data = billiard.forking.get_preparation_data
def wrapper_get_preparation_data(name):
    rez = old_get_preparation_data(name)
    del rez['main_path']
    return rez
billiard.forking.get_preparation_data = wrapper_get_preparation_data
