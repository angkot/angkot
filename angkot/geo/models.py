from django.db import models
from django.utils import timezone

class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)

    # Internal
    enabled = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=True, default=timezone.now)
    created = models.DateTimeField(auto_now=True, default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk',)

