# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gc_toolbox', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cachecoordinates',
            name='type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
