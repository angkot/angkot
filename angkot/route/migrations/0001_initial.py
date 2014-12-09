# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields
import angkot.route.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('submission_id', models.CharField(max_length=64, default=angkot.route.utils.generate_id)),
                ('ip_address', models.IPAddressField(null=True, blank=True, default=None)),
                ('user_agent', models.CharField(null=True, blank=True, max_length=1024, default=None)),
                ('data_version', models.IntegerField(default=1)),
                ('raw_geojson', models.TextField()),
                ('raw_source', models.TextField(null=True, default=None, blank=True)),
                ('province', models.CharField(null=True, blank=True, max_length=5, choices=[('ID-AC', 'Aceh'), ('ID-SU', 'Sumatera Utara'), ('ID-SB', 'Sumatera Barat'), ('ID-RI', 'Riau'), ('ID-JA', 'Jambi'), ('ID-SS', 'Sumatera Selatan'), ('ID-BE', 'Bengkulu'), ('ID-LA', 'Lampung'), ('ID-BB', 'Kepulauan Bangka Belitung'), ('ID-KR', 'Kepulauan Riau'), ('ID-JK', 'Jakarta'), ('ID-JB', 'Jawa Barat'), ('ID-JT', 'Jawa Tengah'), ('ID-YO', 'Yogyakarta'), ('ID-JI', 'Jawa Timur'), ('ID-BT', 'Banten'), ('ID-BA', 'Bali'), ('ID-NB', 'Nusa Tenggara Barat'), ('ID-NT', 'Nusa Tenggara Timur'), ('ID-KB', 'Kalimantan Barat'), ('ID-KT', 'Kalimantan Tengah'), ('ID-KS', 'Kalimantan Selatan'), ('ID-KI', 'Kalimantan Timur'), ('ID-KU', 'Kalimantan Utara'), ('ID-SA', 'Sulawesi Utara'), ('ID-ST', 'Sulawesi Tengah'), ('ID-SN', 'Sulawesi Selatan'), ('ID-SG', 'Sulawesi Tenggara'), ('ID-GO', 'Gorontalo'), ('ID-SR', 'Sulawesi Barat'), ('ID-MA', 'Maluku'), ('ID-MU', 'Maluku Utara'), ('ID-PA', 'Papua'), ('ID-PB', 'Papua Barat')], default=None)),
                ('city', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('company', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('number', models.CharField(null=True, blank=True, max_length=64, default=None)),
                ('origin', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('destination', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('route', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, default=None, blank=True)),
                ('parsed_ok', models.NullBooleanField(default=None)),
                ('parsed_date', models.DateTimeField(null=True, default=None, blank=True)),
                ('parsed_error', models.CharField(null=True, blank=True, max_length=1024, default=None)),
                ('source', models.CharField(null=True, blank=True, max_length=100, default=None)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, to='route.Submission', default=None)),
            ],
            options={
                'ordering': ('-updated',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('province', models.CharField(max_length=5, choices=[('ID-AC', 'Aceh'), ('ID-SU', 'Sumatera Utara'), ('ID-SB', 'Sumatera Barat'), ('ID-RI', 'Riau'), ('ID-JA', 'Jambi'), ('ID-SS', 'Sumatera Selatan'), ('ID-BE', 'Bengkulu'), ('ID-LA', 'Lampung'), ('ID-BB', 'Kepulauan Bangka Belitung'), ('ID-KR', 'Kepulauan Riau'), ('ID-JK', 'Jakarta'), ('ID-JB', 'Jawa Barat'), ('ID-JT', 'Jawa Tengah'), ('ID-YO', 'Yogyakarta'), ('ID-JI', 'Jawa Timur'), ('ID-BT', 'Banten'), ('ID-BA', 'Bali'), ('ID-NB', 'Nusa Tenggara Barat'), ('ID-NT', 'Nusa Tenggara Timur'), ('ID-KB', 'Kalimantan Barat'), ('ID-KT', 'Kalimantan Tengah'), ('ID-KS', 'Kalimantan Selatan'), ('ID-KI', 'Kalimantan Timur'), ('ID-KU', 'Kalimantan Utara'), ('ID-SA', 'Sulawesi Utara'), ('ID-ST', 'Sulawesi Tengah'), ('ID-SN', 'Sulawesi Selatan'), ('ID-SG', 'Sulawesi Tenggara'), ('ID-GO', 'Gorontalo'), ('ID-SR', 'Sulawesi Barat'), ('ID-MA', 'Maluku'), ('ID-MU', 'Maluku Utara'), ('ID-PA', 'Papua'), ('ID-PB', 'Papua Barat')])),
                ('city', models.CharField(max_length=256)),
                ('company', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('number', models.CharField(max_length=64)),
                ('origin', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('destination', models.CharField(null=True, blank=True, max_length=256, default=None)),
                ('route', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, null=True, default=None, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('submission', models.ForeignKey(blank=True, null=True, related_name='used_submission', to='route.Submission', default=None)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='submission',
            name='transportation',
            field=models.ForeignKey(blank=True, null=True, related_name='history', to='route.Transportation', default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(blank=True, null=True, related_name='submitted_route', to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=True,
        ),
    ]
