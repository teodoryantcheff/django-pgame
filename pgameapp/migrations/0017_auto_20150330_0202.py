# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0016_auto_20150330_0144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blockprocessinghistory',
            options={'ordering': ['-timestamp'], 'get_latest_by': 'timestamp', 'verbose_name_plural': 'BlockProcessingHistory'},
        ),
        migrations.AddField(
            model_name='blockprocessinghistory',
            name='blockheight',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 23, 2, 59, 49000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
    ]
