# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0022_auto_20150331_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Date of "official" game start'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='referrer',
            field=models.ForeignKey(related_name='referrals', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
