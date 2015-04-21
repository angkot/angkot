# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='ip_address',
            field=models.GenericIPAddressField(null=True, default=None, blank=True),
        ),
    ]
