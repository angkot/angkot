from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django.utils.translation import ugettext as _

import reversion

from angkot.account.models import Author
from angkot.geo.models import City
from angkot.common.utils.filters import notNone

SRID = 4326

OPT = dict(null=True, default=None, blank=True)

@reversion.register
class Line(models.Model):
    # Data
    type = models.CharField(max_length=1024,
                            help_text=_('Jenis trayek'), **OPT)
    number = models.CharField(max_length=1024, null=False,
                              help_text=_('Nomor trayek'))
    name = models.CharField(max_length=1024,
                            help_text=_('Nama trayek'), **OPT)
    mode = models.CharField(max_length=64,
                            help_text=_('Jenis angkutan (kereta, bis, mikrolet)'), **OPT)

    city = models.ForeignKey(City, **OPT)

    info = HStoreField(**OPT)

    # Author
    author = models.ForeignKey(Author)

    # Internal
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        label = ' '.join(notNone(self.type, self.number))
        if self.city is not None:
            return '{} ({})'.format(label, self.city)
        return label

@reversion.register
class Route(models.Model):
    line = models.ForeignKey(Line)

    # Data
    name = models.CharField(max_length=1024,
                            help_text=_('Nama rute (lokasi berangkat dan tujuan)'), **OPT)
    path = models.LineStringField(srid=SRID, **OPT)
    locations = ArrayField(models.CharField(max_length=1024),
                           help_text=_('Daerah yang dilewati rute'), **OPT)
    order = models.IntegerField(default=0)

    info = HStoreField(**OPT)

    # Author
    author = models.ForeignKey(Author)

    # Internal
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

