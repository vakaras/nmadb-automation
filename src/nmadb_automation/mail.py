#!/usr/bin/python


""" Functions for sending mass mail using celery.
"""


import celery

from django.core import mail
from django import template
from django.utils.html import strip_tags
from django.shortcuts import render

from nmadb_automation.email_multi_related import EmailMultiRelated
from nmadb_automation import forms


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


@celery.task()
def send_template_mail(
        mail_template, to, from_email, context, **backend_args):
    """ Generate and send mail.
    """

    if not isinstance(context, template.Context):
        context = template.Context(context)
    if mail_template.plain_body:
        body = render_template(mail_template.plain_body.name, context)
    else:
        body = None
    email = construct_email(
            template.Template(mail_template.subject).render(context),
            body=body,
            html=render_template(mail_template.html_body.name, context),
            from_email=from_email,
            to=to,
            attachments=[
                (atta.name, atta.attachment_file.read())
                for atta in mail_template.attachment_set.all()
                ],
            inline_attachments=[
                (atta.name, atta.attachment_file.read())
                for atta in mail_template.inlineattachment_set.all()
                ]
            )
    send(email, **backend_args)


@celery.task()
def send_mass_template_mail(
        mail_template, query, from_email, async=True, **backend_args):
    """ Generate and send mass mail.

    Query is an iterable of tuples (to_email, context). If context
    is not an instance of Context then it is passed as argument
    to context.
    """

    if async:
        sender = send_template_mail.delay
    else:
        sender = send_template_mail

    for to, context in query:
        sender(mail_template, [to], from_email, context, **backend_args)


def send_mail_admin_action(make, request, queryset):
    """ Allows to send email.

    Function is intended to be used as admin action.

    ``make`` is a function that given an object from queryset should
    return a list of tuples (email address, context).

    This function makes assumption that primary key of objects in
    queryset is ``id``.
    """
    form = None
    if 'apply' in request.POST:
        form = forms.AdminMailForm(
                request.POST,
                request.FILES)
        if form.is_valid():
            attachments = [
                    (a.name, a.read())
                    for a in request.FILES.getlist('attachments')]
            query = []
            for obj in queryset:
                query.extend(make(obj))
            cd = form.cleaned_data
            send_mass_mail(
                    query, cd['subject'], cd['body'], cd['username'],
                    attachments=attachments,
                    async=len(attachments) == 0,
                    **cd
                    )
            return render(
                    request,
                    'admin/send_email.html',
                    {'form': form})
    if not form:
        form = forms.AdminMailForm(
                initial = {
                    'host': 'smtp.gmail.com',
                    'port': '587',
                    '_selected_action': [
                        unicode(pk)
                        for pk in queryset.values_list('id', flat=True)
                        ]
                    })
    return render(
            request,
            'admin/send_email.html',
            {'form': form})


def send_template_mail_admin_action(make, async, request, queryset):
    """ Sends template email.

    Function is intended to be used as admin action.

    ``make`` is a function that given an object from queryset should
    return a list of tuples (email address, context).

    This function makes assumption that primary key of objects in
    queryset is ``id``.
    """
    form = None
    errors = None
    if 'apply' in request.POST:
        form = forms.AdminTemplateMailForm(request.POST)
        if form.is_valid():
            query = []
            for obj in queryset:
                query.extend(make(obj))
            cd = form.cleaned_data
            try:
                send_mass_template_mail(
                        cd['email_template'],
                        query,
                        cd['username'],
                        async=async,
                        **cd
                        )
            except Exception as e:
                errors = unicode(e)
            return render(
                    request,
                    'admin/send_template_email.html',
                    {'form': form, 'errors': errors, 'async': async})
    if not form:
        form = forms.AdminTemplateMailForm(
                initial={
                    'host': 'smtp.gmail.com',
                    'port': '587',
                    '_selected_action': [
                        unicode(pk)
                        for pk in queryset.values_list('id', flat=True)
                        ]
                    })
    return render(
            request,
            'admin/send_template_email.html',
            {'form': form, 'errors': errors, 'async': async})
