# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Submission.data_version'
        db.add_column('route_submission', 'data_version',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Submission.data_version'
        db.delete_column('route_submission', 'data_version')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'route.submission': {
            'Meta': {'ordering': "('-updated',)", 'object_name': 'Submission'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_version': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'destination': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['route.Submission']", 'null': 'True', 'blank': 'True'}),
            'parsed_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'parsed_error': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'parsed_ok': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'raw_geojson': ('django.db.models.fields.TextField', [], {}),
            'raw_source': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'route': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'submission_id': ('django.db.models.fields.CharField', [], {'default': "'RFRXPK'", 'max_length': '64'}),
            'transportation': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'history'", 'null': 'True', 'blank': 'True', 'to': "orm['route.Transportation']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'submitted_route'", 'null': 'True', 'blank': 'True', 'to': "orm['auth.User']"}),
            'user_agent': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        'route.transportation': {
            'Meta': {'object_name': 'Transportation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'company': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'origin': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'route': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'used_submission'", 'null': 'True', 'blank': 'True', 'to': "orm['route.Submission']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['route']