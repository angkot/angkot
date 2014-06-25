# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('line_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['auth.User'], default=None)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(blank=True, null=True, max_length=15, default=None)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(blank=True, null=True, default=None)),
            ('referer', self.gf('django.db.models.fields.TextField')(blank=True, null=True, default=None)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('line', ['Author'])

        # Adding model 'Line'
        db.create_table('line_line', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=1024, default=None)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=1024, default=None)),
            ('mode', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=64, default=None)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['geo.City'], default=None)),
            ('info', self.gf('django_hstore.fields.DictionaryField')(blank=True, null=True, default=None)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['line.Author'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('line', ['Line'])

        # Adding model 'Route'
        db.create_table('line_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['line.Line'])),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=1024, default=None)),
            ('path', self.gf('django.contrib.gis.db.models.fields.LineStringField')(blank=True, null=True, default=None)),
            ('locations', self.gf('djorm_pgarray.fields.ArrayField')(blank=True, null=True, max_length=1024, default=None, dbtype='varchar')),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['line.Author'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('line', ['Route'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('line_author')

        # Deleting model 'Line'
        db.delete_table('line_line')

        # Deleting model 'Route'
        db.delete_table('line_route')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geo.city': {
            'Meta': {'object_name': 'City', 'ordering': "('province', 'name')"},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Province']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'default': 'datetime.datetime.now'})
        },
        'geo.province': {
            'Meta': {'object_name': 'Province', 'ordering': "('pk',)"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True', 'default': 'datetime.datetime.now'})
        },
        'line.author': {
            'Meta': {'object_name': 'Author'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'blank': 'True', 'null': 'True', 'max_length': '15', 'default': 'None'}),
            'referer': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True', 'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['auth.User']", 'default': 'None'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True', 'default': 'None'})
        },
        'line.line': {
            'Meta': {'object_name': 'Line'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Author']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['geo.City']", 'default': 'None'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django_hstore.fields.DictionaryField', [], {'blank': 'True', 'null': 'True', 'default': 'None'}),
            'mode': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '64', 'default': 'None'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '1024', 'default': 'None'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'type': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '1024', 'default': 'None'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'line.route': {
            'Meta': {'object_name': 'Route'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Author']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Line']"}),
            'locations': ('djorm_pgarray.fields.ArrayField', [], {'blank': 'True', 'null': 'True', 'max_length': '1024', 'default': 'None', 'dbtype': "'varchar'"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '1024', 'default': 'None'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'path': ('django.contrib.gis.db.models.fields.LineStringField', [], {'blank': 'True', 'null': 'True', 'default': 'None'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['line']