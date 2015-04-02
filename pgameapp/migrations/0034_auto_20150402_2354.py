# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0033_auto_20150402_0326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actorprocurementhistory',
            options={'ordering': ['-timestamp'], 'get_latest_by': 'timestamp'},
        ),
        migrations.AlterModelOptions(
            name='coinconversionhistory',
            options={'ordering': ['-timestamp'], 'get_latest_by': 'timestamp'},
        ),
        migrations.AlterModelOptions(
            name='useractorownership',
            options={'ordering': ('actor__price',)},
        ),
        migrations.AlterField(
            model_name='actorprocurementhistory',
            name='user',
            field=models.ForeignKey(related_name='actorprocurementhistory_related', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coinconversionhistory',
            name='user',
            field=models.ForeignKey(related_name='coinconversionhistory_related', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='referralstats',
            name='user',
            field=models.ForeignKey(related_name='referralstats_related', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='user',
            field=models.ForeignKey(related_name='userledger_related', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
