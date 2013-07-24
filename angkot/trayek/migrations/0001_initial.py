# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Kota'
        db.create_table(u'trayek_kota', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'trayek', ['Kota'])

        # Adding model 'Perusahaan'
        db.create_table(u'trayek_perusahaan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nama', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'trayek', ['Perusahaan'])

        # Adding model 'Trayek'
        db.create_table(u'trayek_trayek', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kota', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trayek.Kota'])),
            ('perusahaan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trayek.Perusahaan'])),
            ('nomor', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('awal', self.gf('django.db.models.fields.CharField')(default=None, max_length=128, null=True, blank=True)),
            ('akhir', self.gf('django.db.models.fields.CharField')(default=None, max_length=128, null=True, blank=True)),
            ('rute', self.gf('django.contrib.gis.db.models.fields.LineStringField')(default=None, null=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'trayek', ['Trayek'])

        # Adding model 'Submission'
        db.create_table(u'trayek_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kota', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trayek.Kota'])),
            ('perusahaan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trayek.Perusahaan'])),
            ('nomor', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('awal', self.gf('django.db.models.fields.CharField')(default=None, max_length=128, null=True, blank=True)),
            ('akhir', self.gf('django.db.models.fields.CharField')(default=None, max_length=128, null=True, blank=True)),
            ('rute', self.gf('django.contrib.gis.db.models.fields.LineStringField')(default=None, null=True)),
            ('submission_id', self.gf('django.db.models.fields.CharField')(default='tFKw4D', max_length=64)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True, blank=True)),
            ('visitor_id', self.gf('uuidfield.fields.UUIDField')(default=None, max_length=32, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'trayek', ['Submission'])


    def backwards(self, orm):
        # Deleting model 'Kota'
        db.delete_table(u'trayek_kota')

        # Deleting model 'Perusahaan'
        db.delete_table(u'trayek_perusahaan')

        # Deleting model 'Trayek'
        db.delete_table(u'trayek_trayek')

        # Deleting model 'Submission'
        db.delete_table(u'trayek_submission')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'trayek.kota': {
            'Meta': {'ordering': "('nama',)", 'object_name': 'Kota'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'trayek.perusahaan': {
            'Meta': {'ordering': "('nama',)", 'object_name': 'Perusahaan'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nama': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'trayek.submission': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Submission'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'akhir': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'awal': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kota': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trayek.Kota']"}),
            'nomor': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'perusahaan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trayek.Perusahaan']"}),
            'rute': ('django.contrib.gis.db.models.fields.LineStringField', [], {'default': 'None', 'null': 'True'}),
            'submission_id': ('django.db.models.fields.CharField', [], {'default': "'CGKw4D'", 'max_length': '64'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'visitor_id': ('uuidfield.fields.UUIDField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'trayek.trayek': {
            'Meta': {'ordering': "('kota', 'perusahaan')", 'object_name': 'Trayek'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'akhir': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'awal': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kota': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trayek.Kota']"}),
            'nomor': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'perusahaan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trayek.Perusahaan']"}),
            'rute': ('django.contrib.gis.db.models.fields.LineStringField', [], {'default': 'None', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['trayek']