# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('geo', '0002_auto_20141209_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('type', models.CharField(null=True, max_length=1024, default=None, help_text='Jenis trayek', blank=True)),
                ('number', models.CharField(max_length=1024, help_text='Nomor trayek')),
                ('name', models.CharField(null=True, max_length=1024, default=None, help_text='Nama trayek', blank=True)),
                ('mode', models.CharField(null=True, max_length=64, default=None, help_text='Jenis angkutan', blank=True)),
                ('info', django_hstore.fields.DictionaryField(null=True, default=None, blank=True)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='account.Author')),
                ('city', models.ForeignKey(null=True, default=None, blank=True, to='geo.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(null=True, max_length=1024, default=None, help_text='Nama rute', blank=True)),
                ('path', django.contrib.gis.db.models.fields.LineStringField(null=True, srid=4326, default=None, blank=True)),
                ('locations', djorm_pgarray.fields.ArrayField(null=True, max_length=1024, default=None, help_text='Daerah yang dilewati rute', blank=True)),
                ('ordering', models.IntegerField(default=0)),
                ('info', django_hstore.fields.DictionaryField(null=True, default=None, blank=True)),
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
