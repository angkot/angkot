from django.db import models
from django.utils import timezone

class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    order = models.IntegerField(default=0)

    # Internal
    enabled = models.BooleanField(default=False)
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self):
        self.updated = timezone.now()
        super(Province, self).save()

    class Meta:
        ordering = ('pk',)

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province)

    # Internal
    enabled = models.BooleanField(default=False)
    updated = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}, {}'.format(self.name, self.province)

    def save(self):
        self.updated = timezone.now()
        super(City, self).save()

    class Meta:
        ordering = ('province', 'name',)
        verbose_name_plural = 'cities'

