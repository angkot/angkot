from django.contrib.gis.db import models

class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('pk',)

