# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields.hstore
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        ('account', '0002_auto_20150422_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('type', models.CharField(help_text='Jenis trayek', blank=True, max_length=1024, default=None, null=True)),
                ('number', models.CharField(help_text='Nomor trayek', max_length=1024)),
                ('name', models.CharField(help_text='Nama trayek', blank=True, max_length=1024, default=None, null=True)),
                ('mode', models.CharField(help_text='Jenis angkutan', blank=True, max_length=64, default=None, null=True)),
                ('info', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=None, null=True)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='account.Author')),
                ('city', models.ForeignKey(default=None, null=True, blank=True, to='geo.City')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(help_text='Nama rute', blank=True, max_length=1024, default=None, null=True)),
                ('path', django.contrib.gis.db.models.fields.LineStringField(blank=True, default=None, null=True, srid=4326)),
                ('locations', djorm_pgarray.fields.ArrayField(help_text='Daerah yang dilewati rute', blank=True, max_length=1024, default=None, null=True)),
                ('ordering', models.IntegerField(default=0)),
                ('info', django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=None, null=True)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='account.Author')),
                ('line', models.ForeignKey(to='line.Line')),
            ],
        ),
    ]
