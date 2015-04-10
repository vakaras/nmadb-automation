# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import nmadb_automation.models


class Migration(migrations.Migration):

    dependencies = [
        ('dbtemplates', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='With extension.', max_length=256, verbose_name='file name')),
                ('attachment_file', models.FileField(upload_to=nmadb_automation.models.attachment_upload, verbose_name='attachment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(help_text='You can use Django template syntax.', max_length=256, verbose_name='subject')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('html_body', models.ForeignKey(related_name='+', verbose_name='body in HTML', to='dbtemplates.Template')),
                ('plain_body', models.ForeignKey(related_name='+', blank=True, to='dbtemplates.Template', help_text='If ommited, then it is generated from HTML by removing HTML tags.', null=True, verbose_name='body in plain text')),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InlineAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='With extension.', max_length=256, verbose_name='file name')),
                ('attachment_file', models.FileField(upload_to=nmadb_automation.models.attachment_upload, verbose_name='attachment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('email', models.ForeignKey(verbose_name='email', to='nmadb_automation.Email')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attachment',
            name='email',
            field=models.ForeignKey(verbose_name='email', to='nmadb_automation.Email'),
            preserve_default=True,
        ),
    ]
