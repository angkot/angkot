from django.contrib.gis.db import models
from django.contrib.auth.models import User

from uuidfield import UUIDField

from .utils import generate_id

class Kota(models.Model):
    nama = models.CharField(max_length=128)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.nama

    class Meta:
        ordering = ('nama',)

class Perusahaan(models.Model):
    nama = models.CharField(max_length=128)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.nama

    class Meta:
        ordering = ('nama',)

class Trayek(models.Model):
    kota = models.ForeignKey(Kota)
    perusahaan = models.ForeignKey(Perusahaan)
    nomor = models.CharField(max_length=64)
    awal = models.CharField(max_length=128, null=True,
                            default=None, blank=True)
    akhir = models.CharField(max_length=128, null=True,
                             default=None, blank=True)
    rute = models.LineStringField(null=True, default=None)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{} {}'.format(self.perusahaan, self.nomor)

    class Meta:
        ordering = ('kota', 'perusahaan',)

class Submission(models.Model):
    kota = models.ForeignKey(Kota, null=True, default=None, blank=True)
    perusahaan = models.ForeignKey(Perusahaan, null=True,
                                   default=None, blank=True)
    nomor = models.CharField(max_length=64, null=True, default=None, blank=True)
    awal = models.CharField(max_length=128, null=True,
                            default=None, blank=True)
    akhir = models.CharField(max_length=128, null=True,
                             default=None, blank=True)
    rute = models.LineStringField(null=True, default=None)

    submission_id = models.CharField(max_length=64, default=generate_id)
    user = models.ForeignKey(User, null=True, default=None, blank=True)
    visitor_id = UUIDField(null=True, default=None, blank=True)

    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=1024)
    raw_geojson = models.TextField()

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{} {}'.format(self.perusahaan, self.nomor)

    class Meta:
        ordering = ('-created',)

