from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from django_hstore import hstore

SRID = 4326

OPT = dict(null=True, default=None, blank=True)

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

    def __unicode__(self):
        return "{} ({})".format(self.user, self.ip_address)

class Line(models.Model):
    objects = hstore.HStoreGeoManager()

    # Data
    label = models.CharField(max_length=1024, null=False,
                             help_text=_('Nama angkutan yang dikenal'))
    name = models.CharField(max_length=1024,
                            help_text=_('Nama rute angkutan'), **OPT)
    mode = models.CharField(max_length=64,
                            help_text=_('Jenis angkutan'), **OPT)

    province = models.CharField(max_length=5, choices=PROVINCES, **OPT)
    city = models.CharField(max_length=1024, **OPT)

    info = hstore.DictionaryField(**OPT)

    # Author
    author = models.ForeignKey(Author)

    # Internal
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

class Route(models.Model):
    line = models.ForeignKey(Line)

    # Data
    name = models.CharField(max_length=1024,
                            help_text=_('Nama rute'), **OPT)
    path = models.MultiLineStringField(srid=SRID, **OPT)
    ordering = models.IntegerField(default=0)

    # Author
    author = models.ForeignKey(Author)

    # Internal
    enabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

