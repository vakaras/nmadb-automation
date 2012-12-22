#!/usr/bin/python


""" Functions for sending mass mail using celery.
"""


from celery import task

from django.core import mail
from django.template.loader import get_template


@task()
def send(email, **backend_args):
    """ Send mail asynchronously.

    If ``backend_args`` is provided then uses custom connection.
    """
    if backend_args:
        connection = mail.get_connection(use_tls=True, **backend_args)
        connection.send_messages([email])
    else:
        email.send()


@task()
def render_template(path, context):
    """ Loads template with given path and renders it.
    """
    template = get_template(path)
    return template.render(context)



# TODO: Allow chaining, like: render template | create mail object |
# send it
