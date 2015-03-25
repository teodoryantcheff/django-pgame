# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0003_auto_20150324_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='num_as_bonus',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 25, 16, 6, 7, 942000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
    ]
