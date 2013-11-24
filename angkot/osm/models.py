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

class Way(models.Model):
    id = BigAutoField(primary_key=True)
    osm_id = models.BigIntegerField(unique=True, db_index=True, **optional)

    name = models.CharField(max_length=1024, **optional)
    highway = models.CharField(max_length=256)
    oneway = models.BooleanField(default=False)

    path = models.LineStringField(srid=4326)
    nodes = models.ManyToManyField(Node, related_name='way', through='WayNode')

    # Internal
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class WayNode(models.Model):
    id = BigAutoField(primary_key=True)
    node = BigForeignKey(Node, db_index=True)
    way = BigForeignKey(Way)
    index = models.IntegerField()
    size = models.IntegerField()

