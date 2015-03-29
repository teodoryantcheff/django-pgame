# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0015_auto_20150330_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptotransaction',
            name='crypto_address',
            field=models.CharField(default='', max_length=48),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 22, 44, 26, 996000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
    ]
