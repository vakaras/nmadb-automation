from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from dbtemplates.models import Template as TemplateModel


class Email(models.Model):
    """ Email template for sending.
    """

    subject = models.CharField(
            max_length=256,
            verbose_name=_(u'subject'),
            help_text=_(u'You can use Django template syntax.')
            )

    html_body = models.ForeignKey(
            TemplateModel,
            verbose_name=_(u'body in HTML'),
            related_name=u'+',
            )

    plain_body = models.ForeignKey(
            TemplateModel,
            null=True,
            blank=True,
            verbose_name=_(u'body in plain text'),
            related_name=u'+',
            help_text=_(
                u'If ommited, then it is generated from HTML by '
                u'removing HTML tags.')
            )

    created = models.DateTimeField(
            verbose_name=_('created'),
            auto_now_add=True)

    modified = models.DateTimeField(
            verbose_name=_('modified'),
            auto_now=True)

    class Meta:
        verbose_name = _(u'Email')
        verbose_name_plural = _(u'Emails')

    def __unicode__(self):
        return u'{0.subject} {1}'.format(
                self, self.modified.strftime(u'%Y-%m-%d %H:%M:%S'))


class AttachmentBase(models.Model):
    """ Attachment abstract model.
    """

    def attachment_upload(instance, filename):
        """ Stores attachment in ``attachments/<<name>>/date`` folder.
        """
        return u'attachments/{0.name}/{0.name}'.format(instance)

    name = models.CharField(
            max_length=256,
            verbose_name=_(u'file name'),
            help_text=_(u'With extension.'),
            )

    attachment_file = models.FileField(
            verbose_name=_('attachment'),
            upload_to=attachment_upload,
            )

    created = models.DateTimeField(
            verbose_name=_('created'),
            auto_now_add=True)

    modified = models.DateTimeField(
            verbose_name=_('modified'),
            auto_now=True)

    def __unicode__(self):
        return u'{0.name} ({1})'.format(
                self, self.modified.strftime(u'%Y-%m-%d %H:%M:%S'))

    class Meta:
        abstract = True


class Attachment(AttachmentBase):
    """ Normal email attachment.
    """

    email = models.ForeignKey(
            Email,
            verbose_name=_(u'email')
            )

class InlineAttachment(AttachmentBase):
    """ Inline email attachment.
    """

    email = models.ForeignKey(
            Email,
            verbose_name=_(u'email')
            )
