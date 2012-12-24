# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table('nmadb_automation_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('html_body', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'+', to=orm['dbtemplates.Template'])),
            ('plain_body', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'+', to=orm['dbtemplates.Template'])),
        ))
        db.send_create_signal('nmadb_automation', ['Email'])

        # Adding model 'Attachment'
        db.create_table('nmadb_automation_attachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('attachment_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nmadb_automation.Email'])),
        ))
        db.send_create_signal('nmadb_automation', ['Attachment'])

        # Adding model 'InlineAttachment'
        db.create_table('nmadb_automation_inlineattachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('attachment_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nmadb_automation.Email'])),
        ))
        db.send_create_signal('nmadb_automation', ['InlineAttachment'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table('nmadb_automation_email')

        # Deleting model 'Attachment'
        db.delete_table('nmadb_automation_attachment')

        # Deleting model 'InlineAttachment'
        db.delete_table('nmadb_automation_inlineattachment')


    models = {
        'dbtemplates.template': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Template', 'db_table': "'django_template'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_changed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'})
        },
        'nmadb_automation.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_automation.Email']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'nmadb_automation.email': {
            'Meta': {'object_name': 'Email'},
            'html_body': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['dbtemplates.Template']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plain_body': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['dbtemplates.Template']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'nmadb_automation.inlineattachment': {
            'Meta': {'object_name': 'InlineAttachment'},
            'attachment_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['nmadb_automation.Email']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['nmadb_automation']