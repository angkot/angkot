# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table(u'osm_node', (
            ('id', self.gf('angkot.osm.fields.BigAutoField')(primary_key=True)),
            ('osm_id', self.gf('django.db.models.fields.BigIntegerField')(default=None, unique=True, null=True, db_index=True, blank=True)),
            ('coord', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'osm', ['Node'])

        # Adding model 'Way'
        db.create_table(u'osm_way', (
            ('id', self.gf('angkot.osm.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=1024, null=True, blank=True)),
            ('highway', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('oneway', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('path', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('osm_id', self.gf('django.db.models.fields.BigIntegerField')(default=None, unique=True, null=True, db_index=True, blank=True)),
            ('segments', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'osm', ['Way'])

        # Adding model 'Segment'
        db.create_table(u'osm_segment', (
            ('id', self.gf('angkot.osm.fields.BigAutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=1024, null=True, blank=True)),
            ('highway', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('oneway', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('path', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('osm_id', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, db_index=True, blank=True)),
            ('way', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['osm.Way'])),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'osm', ['Segment'])

        # Adding model 'WayNode'
        db.create_table(u'osm_waynode', (
            ('id', self.gf('angkot.osm.fields.BigAutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('node', self.gf('angkot.osm.fields.BigForeignKey')(to=orm['osm.Node'])),
            ('way', self.gf('angkot.osm.fields.BigForeignKey')(to=orm['osm.Way'])),
        ))
        db.send_create_signal(u'osm', ['WayNode'])

        # Adding model 'SegmentNode'
        db.create_table(u'osm_segmentnode', (
            ('id', self.gf('angkot.osm.fields.BigAutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('node', self.gf('angkot.osm.fields.BigForeignKey')(to=orm['osm.Node'])),
            ('segment', self.gf('angkot.osm.fields.BigForeignKey')(to=orm['osm.Segment'])),
        ))
        db.send_create_signal(u'osm', ['SegmentNode'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table(u'osm_node')

        # Deleting model 'Way'
        db.delete_table(u'osm_way')

        # Deleting model 'Segment'
        db.delete_table(u'osm_segment')

        # Deleting model 'WayNode'
        db.delete_table(u'osm_waynode')

        # Deleting model 'SegmentNode'
        db.delete_table(u'osm_segmentnode')


    models = {
        u'osm.node': {
            'Meta': {'object_name': 'Node'},
            'coord': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('angkot.osm.fields.BigAutoField', [], {'primary_key': 'True'}),
            'osm_id': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'osm.segment': {
            'Meta': {'ordering': "('way', 'index')", 'object_name': 'Segment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'highway': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('angkot.osm.fields.BigAutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'segment'", 'symmetrical': 'False', 'through': u"orm['osm.SegmentNode']", 'to': u"orm['osm.Node']"}),
            'oneway': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'osm_id': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'path': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'way': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['osm.Way']"})
        },
        u'osm.segmentnode': {
            'Meta': {'object_name': 'SegmentNode'},
            'id': ('angkot.osm.fields.BigAutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'node': ('angkot.osm.fields.BigForeignKey', [], {'to': u"orm['osm.Node']"}),
            'segment': ('angkot.osm.fields.BigForeignKey', [], {'to': u"orm['osm.Segment']"}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        u'osm.way': {
            'Meta': {'object_name': 'Way'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'highway': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('angkot.osm.fields.BigAutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'way'", 'symmetrical': 'False', 'through': u"orm['osm.WayNode']", 'to': u"orm['osm.Node']"}),
            'oneway': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'osm_id': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'path': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'segments': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'osm.waynode': {
            'Meta': {'object_name': 'WayNode'},
            'id': ('angkot.osm.fields.BigAutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'node': ('angkot.osm.fields.BigForeignKey', [], {'to': u"orm['osm.Node']"}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'way': ('angkot.osm.fields.BigForeignKey', [], {'to': u"orm['osm.Way']"})
        }
    }

    complete_apps = ['osm']