from django.contrib.auth.models import User
from django.contrib.gis.db import models

from ipware.ip import get_ip

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

