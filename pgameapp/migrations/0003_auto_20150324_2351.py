# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0002_gameconfiguration_game_start_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 24, 21, 51, 12, 596000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
    ]
