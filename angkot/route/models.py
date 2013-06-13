from django.contrib.gis.db import models
from django.contrib.auth.models import User

from uuidfield import UUIDField

from .utils import generate_route_id

class Route(models.Model):
    route_id = models.CharField(max_length=10, unique=True,
                                default=generate_route_id)

    user = models.ForeignKey(User, null=True, default=None, blank=True)
    visitor_id = UUIDField(null=True, default=None, blank=True)

    vehicle_type = models.CharField(max_length=100, null=True, blank=True)
    transportation_name = models.CharField(max_length=100, null=True)
    origin = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    path = models.LineStringField(null=True, default=None)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.transportation_name

