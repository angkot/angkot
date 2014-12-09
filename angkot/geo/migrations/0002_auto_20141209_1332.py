# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_provinces(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "geo_provinces.yaml")

class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_provinces)
    ]
