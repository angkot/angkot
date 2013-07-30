from django.contrib.gis.db import models
from django.contrib.auth.models import User

from uuidfield import UUIDField

from .utils import generate_id

class Submission(models.Model):
    optional = dict(null=True, default=None, blank=True)

    # Meta
    submission_id = models.CharField(max_length=64, default=generate_id)
    user = models.ForeignKey(User, related_name='submitted_route', **optional)
    visitor_id = UUIDField()
    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=1024)

    # Submitted data
    parent = models.ForeignKey('self', **optional)
    raw_geojson = models.TextField()

    # Parsed data
    city = models.CharField(max_length=256, **optional)
    company = models.CharField(max_length=256, **optional)
    number = models.CharField(max_length=64, **optional)
    origin = models.CharField(max_length=256, **optional)
    destination = models.CharField(max_length=256, **optional)
    route = models.MultiLineStringField(**optional)

    parsed_ok = models.NullBooleanField(**optional)
    parsed_date = models.DateTimeField(**optional)
    parsed_error = models.CharField(max_length=1024, **optional)

    # Internal
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated',)

    def to_geojson(self):
        import geojson
        from shapely.geometry import asMultiLineString

        if self.route is not None:
            p = asMultiLineString(self.route)
            geometry = geojson.loads(geojson.dumps(p))
        else:
            geometry = {
                'type': 'MultiLineString',
                'coordinates': []
            }

        return {
            'type': 'Feature',
            'properties': {
                'city': self.city,
                'company': self.company,
                'number': self.number,
                'origin': self.origin,
                'destination': self.destination,
            },
            'geometry': geometry
        }

