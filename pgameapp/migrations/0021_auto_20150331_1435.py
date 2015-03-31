# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0020_auto_20150331_0246'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='userprofile',
        #     name='id',
        # ),
        migrations.AddField(
            model_name='userprofile',
            name='ref_campaign',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ref_source',
            field=models.CharField(default=b'', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 31, 11, 35, 0, 43000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
