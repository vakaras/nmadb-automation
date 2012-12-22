"""
A slightly modified version of this snippet:
http://djangosnippets.org/snippets/2215/.
"""


import os.path
import re

from email.MIMEBase import MIMEBase

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart


class EmailMultiRelated(EmailMultiAlternatives):
    """
    A version of EmailMessage that makes it easy to send
    multipart/related messages. For example, including text and HTML
    versions with inline images.
    """
    related_subtype = 'related'

    def __init__(
            self, subject='', body='', from_email=None, to=None,
            bcc=None, connection=None, attachments=None, headers=None,
            alternatives=None):
        # self.related_ids = []
        self.related_attachments = []
        return super(EmailMultiRelated, self).__init__(
                subject, body, from_email, to, bcc, connection,
                attachments, headers, alternatives)

    def attach_related(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The
        filename can be omitted and the mimetype is guessed, if not
        provided.

        If the first parameter is a MIMEBase subclass it is inserted
        directly into the resulting message attachments.
        """
        if isinstance(filename, MIMEBase):
            assert content == mimetype == None
            self.related_attachments.append(filename)
        else:
            assert content is not None
            self.related_attachments.append((filename, content, mimetype))

    def attach_related_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, 'rb').read()
        self.attach_related(filename, content, mimetype)

    def _create_message(self, msg):
        alternative = self._create_alternatives(msg)
        related_attachment = self._create_related_attachments(alternative)
        return self._create_attachments(related_attachment)

    def _create_alternatives(self, msg):
        for i, (content, mimetype) in enumerate(self.alternatives):
            if mimetype == 'text/html':
                for filename, _, _ in self.related_attachments:
                    expr = r'(?<!cid:)%s' % re.escape(filename)
                    change = 'cid:%s' % filename
                    content = re.sub(expr, change, content)
                self.alternatives[i] = (content, mimetype)
        return super(EmailMultiRelated, self)._create_alternatives(msg)

    def _create_related_attachments(self, msg):
        encoding = self.encoding or settings.DEFAULT_CHARSET
        if self.related_attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(
                    _subtype=self.related_subtype,
                    encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for related in self.related_attachments:
                msg.attach(self._create_related_attachment(*related))
        return msg

    def _create_related_attachment(self, filename, content, mimetype=None):
        """
        Convert the filename, content, mimetype triple into a MIME
        attachment object. Adjust headers to use Content-ID where
        applicable. Taken from http://code.djangoproject.com/ticket/4771
        """
        attachment = super(EmailMultiRelated, self)._create_attachment(
                filename, content, mimetype)
        if filename:
            mimetype = attachment['Content-Type']
            del(attachment['Content-Type'])
            del(attachment['Content-Disposition'])
            attachment.add_header(
                    'Content-Disposition',
                    'inline',
                    filename=filename)
            attachment.add_header('Content-Type', mimetype, name=filename)
            attachment.add_header('Content-ID', '<%s>' % filename)
        return attachment
