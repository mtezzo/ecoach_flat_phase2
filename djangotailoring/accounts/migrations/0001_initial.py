# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GroupAccessCode'
        db.create_table('accounts_groupaccesscode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('groupcode', self.gf('django.db.models.fields.TextField')(max_length=6)),
            ('usage_limit', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal('accounts', ['GroupAccessCode'])

        # Adding model 'GeneratedAccessCode'
        db.create_table('accounts_generatedaccesscode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accesscode', self.gf('django.db.models.fields.TextField')(max_length=6)),
            ('groupcode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.GroupAccessCode'])),
        ))
        db.send_create_signal('accounts', ['GeneratedAccessCode'])


    def backwards(self, orm):
        
        # Deleting model 'GroupAccessCode'
        db.delete_table('accounts_groupaccesscode')

        # Deleting model 'GeneratedAccessCode'
        db.delete_table('accounts_generatedaccesscode')


    models = {
        'accounts.generatedaccesscode': {
            'Meta': {'object_name': 'GeneratedAccessCode'},
            'accesscode': ('django.db.models.fields.TextField', [], {'max_length': '6'}),
            'groupcode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.GroupAccessCode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'accounts.groupaccesscode': {
            'Meta': {'object_name': 'GroupAccessCode'},
            'groupcode': ('django.db.models.fields.TextField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usage_limit': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        }
    }

    complete_apps = ['accounts']
