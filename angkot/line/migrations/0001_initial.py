# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django_hstore.fields
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('geo', '0002_auto_20141209_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1024, null=True, help_text='Jenis trayek', blank=True, default=None)),
                ('number', models.CharField(max_length=1024, help_text='Nomor trayek')),
                ('name', models.CharField(max_length=1024, null=True, help_text='Nama trayek', blank=True, default=None)),
                ('mode', models.CharField(max_length=64, null=True, help_text='Jenis angkutan', blank=True, default=None)),
                ('info', django_hstore.fields.DictionaryField(null=True, blank=True, default=None)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='account.Author')),
                ('city', models.ForeignKey(null=True, to='geo.City', default=None, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024, null=True, help_text='Nama rute', blank=True, default=None)),
                ('path', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, blank=True, default=None)),
                ('locations', djorm_pgarray.fields.ArrayField(max_length=1024, null=True, help_text='Daerah yang dilewati rute', blank=True, default=None)),
                ('ordering', models.IntegerField(default=0)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='account.Author')),
                ('line', models.ForeignKey(to='line.Line')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
