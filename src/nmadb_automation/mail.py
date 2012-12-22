#!/usr/bin/python


""" Functions for sending mass mail using celery.
"""


import celery

from django.core import mail
from django import template
from django.utils.html import strip_tags

from nmadb_automation.email_multi_related import EmailMultiRelated


@celery.task()
def send(email, **backend_args):
    """ Send mail asynchronously.

    If ``backend_args`` is provided then uses custom connection.
    """
    if backend_args:
        connection = mail.get_connection(use_tls=True, **backend_args)
        connection.send_messages([email])
    else:
        email.send()


@celery.task()
def render_template(path, context):
    """ Loads template with given path and renders it.
    """
    templ = template.loader.get_template(path)
    return templ.render(context)


@celery.task()
def construct_email(subject='', body='', *args, **kwargs):
    """ Construct email object.

    Parameters are the same as for EmailMultiRelated constructor,
    except that it additionally supports:

    +   html -- message text in html. Additionally, if ``body`` is not
        provided, then it is generated from ``html`` by striping
        ``html`` tags.
    """
    if 'html' in kwargs:
        html = kwargs['html']
        del kwargs['html']
        if not body:
            body = strip_tags(html)
    else:
        html = None
    if 'attachments' in kwargs:
        attachments = kwargs['attachments']
        del kwargs['attachments']
    else:
        attachments = ()
    if 'inline_attachments' in kwargs:
        inline_attachments = kwargs['inline_attachments']
        del kwargs['inline_attachments']
    else:
        inline_attachments = ()
    email = EmailMultiRelated(subject, body, *args, **kwargs)
    if html:
        email.attach_alternative(html, 'text/html')
    for attachment in attachments:
        email.attach(*attachment)
    for attachment in inline_attachments:
        email.attach_related(*attachment)
    return email


@celery.task()
def send_mass_mail(
        query, subject_template, body_template, from_email,
        attachments=(), inline_attachments=(), async=True, **backend_args):
    """ Asynchronously sends mass mail.

    Query is an iterable of tuples (to_email, context). If context
    is not an instance of Context then it is passed as argument
    to context.
    """

    if not isinstance(subject_template, template.Template):
        subject_template = template.Template(subject_template)
    if not isinstance(body_template, template.Template):
        body_template = template.Template(body_template)
    if async:
        constructor = construct_email.s
    else:
        constructor = construct_email

    for to, context in query:
        if not isinstance(context, template.Context):
            context = template.Context(context)
        email = constructor(
                subject_template.render(context),
                html=body_template.render(context),
                from_email=from_email,
                to=[to],
                attachments=attachments,
                inline_attachments=inline_attachments
                )
        if async:
            celery.chain(email, send.s(**backend_args))()
        else:
            send(email, **backend_args)
