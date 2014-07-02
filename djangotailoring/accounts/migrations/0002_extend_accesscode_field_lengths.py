# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'GeneratedAccessCode.accesscode'
        db.alter_column('accounts_generatedaccesscode', 'accesscode', self.gf('django.db.models.fields.TextField')(max_length=30))

        # Changing field 'GroupAccessCode.groupcode'
        db.alter_column('accounts_groupaccesscode', 'groupcode', self.gf('django.db.models.fields.TextField')(max_length=30))


    def backwards(self, orm):
        
        # Changing field 'GeneratedAccessCode.accesscode'
        db.alter_column('accounts_generatedaccesscode', 'accesscode', self.gf('django.db.models.fields.TextField')(max_length=6))

        # Changing field 'GroupAccessCode.groupcode'
        db.alter_column('accounts_groupaccesscode', 'groupcode', self.gf('django.db.models.fields.TextField')(max_length=6))


    models = {
        'accounts.generatedaccesscode': {
            'Meta': {'object_name': 'GeneratedAccessCode'},
            'accesscode': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'groupcode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.GroupAccessCode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'accounts.groupaccesscode': {
            'Meta': {'object_name': 'GroupAccessCode'},
            'groupcode': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usage_limit': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        }
    }

    complete_apps = ['accounts']
