from django.contrib import admin
from django.utils.translation import ugettext as _

from nmadb_utils import admin as utils
from nmadb_automation import models


class AttachmentInline(admin.TabularInline):
    """ Inline attachment administration.
    """

    model = models.Attachment

    extra = 3


class InlineAttachmentInline(admin.TabularInline):
    """ Inline attachment administration.
    """

    model = models.InlineAttachment

    extra = 3


class EmailAdmin(utils.ModelAdmin):
    """ Administration for emails.
    """

    inlines = [
            AttachmentInline,
            InlineAttachmentInline,
            ]

    list_display = (
            'id',
            'subject',
            )


admin.site.register(models.Email, EmailAdmin)
