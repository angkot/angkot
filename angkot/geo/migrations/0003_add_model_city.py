# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table('geo_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Province'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('geo', ['City'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table('geo_city')


    models = {
        'geo.city': {
            'Meta': {'object_name': 'City', 'ordering': "('province', 'name')"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Province']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'geo.province': {
            'Meta': {'object_name': 'Province', 'ordering': "('pk',)"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geo']