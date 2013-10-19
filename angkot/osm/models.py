from django.contrib.gis.db import models

from .fields import BigAutoField, BigForeignKey

optional = dict(null=True, default=None, blank=True)

class Node(models.Model):
    id = BigAutoField(primary_key=True)
    osm_id = models.BigIntegerField(unique=True, db_index=True, **optional)

    coord = models.PointField(srid=4326)

    # Internal
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class BaseWay(models.Model):
    id = BigAutoField(primary_key=True)

    name = models.CharField(max_length=1024, **optional)
    highway = models.CharField(max_length=256)
    oneway = models.BooleanField(default=False)

    path = models.LineStringField(srid=4326)

    # Internal
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Way(BaseWay):
    osm_id = models.BigIntegerField(unique=True, db_index=True, **optional)
    nodes = models.ManyToManyField(Node, related_name='way', through='WayNode')

    segments = models.IntegerField()

class Segment(BaseWay):
    osm_id = models.BigIntegerField(db_index=True, **optional)
    way = models.ForeignKey(Way, db_index=True)
    index = models.IntegerField()
    size = models.IntegerField()

    nodes = models.ManyToManyField(Node, related_name='segment', through='SegmentNode')

    class Meta:
        ordering = ('way', 'index',)

class BaseWayNode(models.Model):
    id = BigAutoField(primary_key=True)

    index = models.IntegerField()
    size = models.IntegerField()

    class Meta:
        abstract = True

class WayNode(BaseWayNode):
    node = BigForeignKey(Node, db_index=True)
    way = BigForeignKey(Way)

class SegmentNode(BaseWayNode):
    node = BigForeignKey(Node, db_index=True)
    segment = BigForeignKey(Segment)

