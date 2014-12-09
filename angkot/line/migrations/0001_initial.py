# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields
from django.conf import settings
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ip_address', models.IPAddressField(null=True, blank=True, default=None)),
                ('user_agent', models.TextField(null=True, default=None, blank=True)),
                ('referer', models.TextField(null=True, default=None, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(null=True, default=None, blank=True, max_length=1024, help_text='Jenis trayek')),
                ('number', models.CharField(max_length=1024, help_text='Nomor trayek')),
                ('name', models.CharField(null=True, default=None, blank=True, max_length=1024, help_text='Nama trayek')),
                ('mode', models.CharField(null=True, default=None, blank=True, max_length=64, help_text='Jenis angkutan')),
                ('info', django_hstore.fields.DictionaryField(null=True, default=None, blank=True)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='line.Author')),
                ('city', models.ForeignKey(blank=True, null=True, to='geo.City', default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(null=True, default=None, blank=True, max_length=1024, help_text='Nama rute')),
                ('path', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, default=None, blank=True)),
                ('locations', djorm_pgarray.fields.ArrayField(null=True, default=None, blank=True, max_length=1024, help_text='Daerah yang dilewati rute')),
                ('ordering', models.IntegerField(default=0)),
                ('enabled', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='line.Author')),
                ('line', models.ForeignKey(to='line.Line')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
