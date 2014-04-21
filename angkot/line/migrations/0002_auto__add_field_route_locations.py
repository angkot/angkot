# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Route.locations'
        db.add_column('line_route', 'locations',
                      self.gf('djorm_pgarray.fields.ArrayField')(max_length=1024, dbtype='varchar', blank=True, default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Route.locations'
        db.delete_column('line_route', 'locations')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'line.author': {
            'Meta': {'object_name': 'Author'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'referer': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['auth.User']", 'default': 'None', 'null': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'blank': 'True', 'default': 'None', 'null': 'True'})
        },
        'line.line': {
            'Meta': {'object_name': 'Line'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Author']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django_hstore.fields.DictionaryField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        },
        'line.route': {
            'Meta': {'object_name': 'Route'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Author']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Line']"}),
            'locations': ('djorm_pgarray.fields.ArrayField', [], {'max_length': '1024', 'dbtype': "'varchar'", 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'path': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'})
        }
    }

    complete_apps = ['line']