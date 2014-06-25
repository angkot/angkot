from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

import reversion
from django_hstore import hstore
from djorm_pgarray.fields import ArrayField

from angkot.geo.models import City
from angkot.common.utils.filters import notNone

SRID = 4326

OPT = dict(null=True, default=None, blank=True)

class AuthorManager(models.Manager):
    def create_internal(self, source=None):
        author = Author()
        author.user = None
        author.ip_address = '0.0.0.0'
        author.user_agent = 'Angkot Internal'
        author.referer = source
        author.save(using=self._db)
        return author

    def create_from_request(self, request):
        from ipware.ip import get_ip

        author = Author()
        author.user = request.user
        author.ip_address = get_ip(request)
        author.user_agent = request.META.get('HTTP_USER_AGENT')
        author.referer = request.META.get('HTTP_REFERER')
        author.save(using=self._db)
        return author

class Author(models.Model):
    objects = AuthorManager()

    # Data
    user = models.ForeignKey(User, **OPT)

    ip_address = models.IPAddressField(**OPT)
    user_agent = models.TextField(**OPT)
    referer = models.TextField(**OPT)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ({})".format(self.user, self.ip_address)

class Line(models.Model):
    objects = hstore.HStoreGeoManager()

    # Data
    type = models.CharField(max_length=1024,
                            help_text=_('Jenis trayek'), **OPT)
    number = models.CharField(max_length=1024, null=False,
                              help_text=_('Nomor trayek'))
    name = models.CharField(max_length=1024,
                            help_text=_('Nama trayek'), **OPT)
    mode = models.CharField(max_length=64,
                            help_text=_('Jenis angkutan'), **OPT)

    city = models.ForeignKey(City, **OPT)

    info = hstore.DictionaryField(**OPT)

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

reversion.register(Line)

class Route(models.Model):
    line = models.ForeignKey(Line)

    # Data
    name = models.CharField(max_length=1024,
                            help_text=_('Nama rute'), **OPT)
    path = models.LineStringField(srid=SRID, **OPT)
    locations = ArrayField(dbtype="varchar", max_length=1024,
                           help_text=_('Daerah yang dilewati rute'))
    ordering = models.IntegerField(default=0)

    # Author
    author = models.ForeignKey(Author)

    # Internal
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

reversion.register(Route)

