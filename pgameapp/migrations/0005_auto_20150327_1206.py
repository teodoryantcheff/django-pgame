# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0004_auto_20150325_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actor',
            name='num_as_bonus',
            field=models.PositiveIntegerField(default=0, verbose_name=b'as bonus'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actor',
            name='output',
            field=models.FloatField(default=0, verbose_name=b'output / h'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 27, 10, 6, 25, 969000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
    ]
