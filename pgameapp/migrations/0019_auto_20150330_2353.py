# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0018_auto_20150330_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 20, 53, 35, 890000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='referrer',
            field=models.ForeignKey(related_name='referrals', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
