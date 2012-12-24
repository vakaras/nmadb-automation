#! -*- encoding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

from nmadb_automation import models


class AdminMailFormMixin(forms.Form):
    """ Mixin that allows to transfer selection.
    """
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)


class CustomServerMixin(forms.Form):
    """ Form fields that allow to send email by using custom SMTP server.
    """
    host = forms.CharField(
            label=_(u'SMTP server'))
    username = forms.CharField(
            label=_(u'username'))
    password = forms.CharField(
            widget=forms.PasswordInput(),
            label=_(u'password'))
    port = forms.IntegerField(
            label=_(u'port'))

    def clean_password(self):
        """ Checks if password is not too long.
        """

        try:
            password = str(self.cleaned_data['password'])
        except UnicodeEncodeError:
            raise forms.ValidationError((
                _(u'Server does not support Unicode passwords.')))
        if len(password) > 16:
            raise forms.ValidationError(
                _(u'Password is longer than 16 symbols.'))
        return password


class TemplateMixin(forms.Form):
    """ Form fields that allow to select Mail template.
    """

    email_template = forms.ModelChoiceField(
            models.Email.objects,
            label=_('email template'),
            )


class BaseMailForm(forms.Form):
    """ Basic mail form.
    """

    subject = forms.CharField(label=_(u'subject'))
    body = forms.CharField(widget=forms.Textarea(), label=_(u'body'))


class AdminMailForm(AdminMailFormMixin, CustomServerMixin, BaseMailForm):
    """ Mail form for using in Django admin.
    """


class AdminTemplateMailForm(
        AdminMailFormMixin,
        CustomServerMixin,
        TemplateMixin):
    """ Mail form for using in Django admin.
    """


class MailCreateForm(forms.Form):
    """ Basic mail form.
    """

    name = forms.CharField(
            label=_(u'template name'),
            help_text=_(
                u'“mail” directory and file extension will be '
                u'appended automatically.')
            )
    subject = forms.CharField(label=_(u'subject'))
    body = forms.CharField(widget=forms.Textarea(), label=_(u'body'))
