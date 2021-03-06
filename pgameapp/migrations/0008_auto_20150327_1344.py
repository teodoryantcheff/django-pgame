# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0007_auto_20150327_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='singnup_ip',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='signup_ip',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 27, 11, 44, 13, 437000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
    ]
