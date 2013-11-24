# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Segment'
        db.delete_table(u'osm_segment')

        # Deleting model 'SegmentNode'
        db.delete_table(u'osm_segmentnode')

        # Deleting field 'Way.segments'
        db.delete_column(u'osm_way', 'segments')


    def backwards(self, orm):
        # Adding model 'Segment'
        db.create_table(u'osm_segment', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('osm_id', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True, db_index=True)),
            ('path', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
            ('id', self.gf('angkot.osm.fields.BigAutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=1024, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('way', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['osm.Way'])),
            ('oneway', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('highway', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'osm', ['Segment'])

        # Adding model 'SegmentNode'
        db.create_table(u'osm_segmentnode', (
            ('node', self.gf('angkot.osm.fields.BigForeignKey')(to=orm['osm.Node'])),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('segment', self.gf('angkot.osm.fields.BigForeignKey')(to=orm['osm.Segment'])),
            ('id', self.gf('angkot.osm.fields.BigAutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'osm', ['SegmentNode'])


        # User chose to not deal with backwards NULL issues for 'Way.segments'
        raise RuntimeError("Cannot reverse this migration. 'Way.segments' and its values cannot be restored.")

    models = {
        u'osm.node': {
            'Meta': {'object_name': 'Node'},
            'coord': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('angkot.osm.fields.BigAutoField', [], {'primary_key': 'True'}),
            'osm_id': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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