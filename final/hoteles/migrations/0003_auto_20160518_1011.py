# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0002_auto_20160518_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='estrellas',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alojamiento',
            name='categoria',
            field=models.CharField(max_length=16),
        ),
    ]
