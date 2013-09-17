from django.contrib.gis.db import models
from django.contrib.auth.models import User

from uuidfield import UUIDField

from .utils import generate_id

PROVINCES = (
    ('ID-AC', 'Aceh'),
    ('ID-SU', 'Sumatera Utara'),
    ('ID-SB', 'Sumatera Barat'),
    ('ID-RI', 'Riau'),
    ('ID-JA', 'Jambi'),
    ('ID-SS', 'Sumatera Selatan'),
    ('ID-BE', 'Bengkulu'),
    ('ID-LA', 'Lampung'),
    ('ID-BB', 'Kepulauan Bangka Belitung'),
    ('ID-KR', 'Kepulauan Riau'),
    ('ID-JK', 'Jakarta'),
    ('ID-JB', 'Jawa Barat'),
    ('ID-JT', 'Jawa Tengah'),
    ('ID-YO', 'Yogyakarta'),
    ('ID-JI', 'Jawa Timur'),
    ('ID-BT', 'Banten'),
    ('ID-BA', 'Bali'),
    ('ID-NB', 'Nusa Tenggara Barat'),
    ('ID-NT', 'Nusa Tenggara Timur'),
    ('ID-KB', 'Kalimantan Barat'),
    ('ID-KT', 'Kalimantan Tengah'),
    ('ID-KS', 'Kalimantan Selatan'),
    ('ID-KI', 'Kalimantan Timur'),
    ('ID-KU', 'Kalimantan Utara'),
    ('ID-SA', 'Sulawesi Utara'),
    ('ID-ST', 'Sulawesi Tengah'),
    ('ID-SN', 'Sulawesi Selatan'),
    ('ID-SG', 'Sulawesi Tenggara'),
    ('ID-GO', 'Gorontalo'),
    ('ID-SR', 'Sulawesi Barat'),
    ('ID-MA', 'Maluku'),
    ('ID-MU', 'Maluku Utara'),
    ('ID-PA', 'Papua'),
    ('ID-PB', 'Papua Barat'),
)

class Transportation(models.Model):
    optional = dict(null=True, default=None, blank=True)

    # Data
    province = models.CharField(max_length=5, choices=PROVINCES)
    city = models.CharField(max_length=256)
    company = models.CharField(max_length=256, **optional)
    number = models.CharField(max_length=64)
    origin = models.CharField(max_length=256, **optional)
    destination = models.CharField(max_length=256, **optional)
    route = models.MultiLineStringField(**optional)

    submission = models.ForeignKey('Submission', related_name='used_submission', **optional)

    # Internal
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{} {} - {}'.format(self.company, self.number, self.city)

    def to_geojson(self):
        from . import utils
        return utils.to_geojson(self)

class Submission(models.Model):
    optional = dict(null=True, default=None, blank=True)

    # Meta
    submission_id = models.CharField(max_length=64, default=generate_id)
    user = models.ForeignKey(User, related_name='submitted_route', **optional)
    ip_address = models.IPAddressField(**optional)
    user_agent = models.CharField(max_length=1024, **optional)
    transportation = models.ForeignKey(Transportation, related_name='history', **optional)

    # Submitted data
    parent = models.ForeignKey('self', **optional)
    raw_geojson = models.TextField()
    raw_source = models.TextField(**optional)

    # Parsed data
    province = models.CharField(max_length=5, choices=PROVINCES, **optional)
    city = models.CharField(max_length=256, **optional)
    company = models.CharField(max_length=256, **optional)
    number = models.CharField(max_length=64, **optional)
    origin = models.CharField(max_length=256, **optional)
    destination = models.CharField(max_length=256, **optional)
    route = models.MultiLineStringField(**optional)

    parsed_ok = models.NullBooleanField(**optional)
    parsed_date = models.DateTimeField(**optional)
    parsed_error = models.CharField(max_length=1024, **optional)

    source = models.CharField(max_length=100, **optional)

    # Internal
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{} {} - {} - {}'.format(self.company, self.number, self.city, self.user)

    class Meta:
        ordering = ('-updated',)

    def to_geojson(self):
        from . import utils
        return utils.to_geojson(self)

