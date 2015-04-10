import os
import urllib
from django.utils import timezone

from django.core.files import File
from django.contrib import admin
from django.db import transaction
from annoying.decorators import render_to
from django import shortcuts
from dbtemplates.models import Template
from django.utils.html import strip_tags
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from bs4 import BeautifulSoup

from nmadb_automation import forms, models


@admin.site.admin_view
@render_to('admin/file-form.html')
@transaction.atomic
def create_mail(request):
    """ Creates mail template from HTML document.
    """
    errors = None
    if request.method == 'POST':
        form = forms.MailCreateForm(request.POST)
        if form.is_valid():
            html_body = form.cleaned_data['body']
            soup = BeautifulSoup(html_body)
            inline_attachments = []
            try:
                for image in soup.find_all('img'):
                    src = image.get("src")
                    if src:
                        attachment = models.InlineAttachment()
                        attachment.name = os.path.basename(src)
                        attachment.created = timezone.now()
                        attachment.attachment_file.save(
                                attachment.name,
                                File(open(urllib.urlretrieve(src)[0])),
                                save=False)
                        inline_attachments.append(attachment)
                        image['src'] = u'cid:{0}'.format(attachment.name)
            except Exception as e:
                errors = unicode(e)
                raise
            email = models.Email()
            email.subject = form.cleaned_data['subject']
            html_body_template = Template()
            html_body_template.name = u'mail/{0}.html'.format(
                    form.cleaned_data[u'name'])
            html_body_template.content = soup.prettify()
            html_body_template.save()
            email.html_body = html_body_template
            plain_body_template = Template()
            plain_body_template.name = u'mail/{0}.txt'.format(
                    form.cleaned_data[u'name'])
            plain_body_template.content = soup.get_text()
            plain_body_template.save()
            email.plain_body = plain_body_template
            email.save()
            for attachment in inline_attachments:
                attachment.email = email
                attachment.save()

        return shortcuts.redirect(
                'admin:nmadb_automation_email_changelist')
    else:
        form = forms.MailCreateForm()
    return {
            'admin_index_url': urlresolvers.reverse('admin:index'),
            'app_url': urlresolvers.reverse(
                'admin:app_list',
                kwargs={'app_label': 'nmadb_automation'}),
            'app_label': _(u'NMADB Automation'),
            'form': form,
            'errors': errors,
            }
