# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.hstore


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20141209_1332'),
        ('account', '0002_auto_20150422_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('type', models.CharField(null=True, help_text='Jenis trayek', blank=True, default=None, max_length=1024)),
                ('number', models.CharField(help_text='Nomor trayek', max_length=1024)),
                ('name', models.CharField(null=True, help_text='Nama trayek', blank=True, default=None, max_length=1024)),
                ('mode', models.CharField(null=True, help_text='Jenis angkutan (kereta, bis, mikrolet)', blank=True, default=None, max_length=64)),
                ('info', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True, default=None)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='account.Author')),
                ('city', models.ForeignKey(null=True, blank=True, to='geo.City', default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(null=True, help_text='Nama rute (lokasi berangkat dan tujuan)', blank=True, default=None, max_length=1024)),
                ('path', django.contrib.gis.db.models.fields.LineStringField(null=True, blank=True, default=None, srid=4326)),
                ('locations', django.contrib.postgres.fields.ArrayField(null=True, blank=True, size=None, base_field=models.CharField(max_length=1024), help_text='Daerah yang dilewati rute', default=None)),
                ('ordering', models.IntegerField(default=0)),
                ('info', django.contrib.postgres.fields.hstore.HStoreField(null=True, blank=True, default=None)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='account.Author')),
                ('line', models.ForeignKey(to='line.Line')),
            ],
        ),
    ]
