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
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, blank=True, to=orm['auth.User'], null=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, default=None, blank=True, null=True)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(default=None, blank=True, null=True)),
            ('referer', self.gf('django.db.models.fields.TextField')(default=None, blank=True, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('line', ['Author'])

        # Adding model 'Line'
        db.create_table('line_line', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1024, default=None, blank=True, null=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, default=None, blank=True, null=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=64, default=None, blank=True, null=True)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(default=None, blank=True, to=orm['geo.Province'], null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=1024, default=None, blank=True, null=True)),
            ('info', self.gf('django_hstore.fields.DictionaryField')(default=None, blank=True, null=True)),
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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024, default=None, blank=True, null=True)),
            ('path', self.gf('django.contrib.gis.db.models.fields.LineStringField')(default=None, blank=True, null=True)),
            ('locations', self.gf('djorm_pgarray.fields.ArrayField')(max_length=1024, default=None, blank=True, dbtype='varchar', null=True)),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geo.province': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'Province'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'line.author': {
            'Meta': {'object_name': 'Author'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'referer': ('django.db.models.fields.TextField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'blank': 'True', 'to': "orm['auth.User']", 'null': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'default': 'None', 'blank': 'True', 'null': 'True'})
        },
        'line.line': {
            'Meta': {'object_name': 'Line'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Author']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django_hstore.fields.DictionaryField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '64', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'blank': 'True', 'to': "orm['geo.Province']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'line.route': {
            'Meta': {'object_name': 'Route'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Author']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['line.Line']"}),
            'locations': ('djorm_pgarray.fields.ArrayField', [], {'max_length': '1024', 'default': 'None', 'blank': 'True', 'dbtype': "'varchar'", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'default': 'None', 'blank': 'True', 'null': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'path': ('django.contrib.gis.db.models.fields.LineStringField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['line']