# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('enabled', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now=True, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'cities',
                'ordering': ('province', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=5)),
                ('enabled', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now=True, default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('pk',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(to='geo.Province'),
            preserve_default=True,
        ),
    ]
