# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0034_auto_20150402_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referralstats',
            name='referred_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='type',
            field=models.CharField(max_length=10, choices=[(b'pmt', b'payment'), (b'b_rp', b'referral payment'), (b'b_fp', b'1st payment bonus'), (b'wdr', b'withdrawal'), (b'bac', b'buy actor'), (b'w2i', b'w2i'), (b'sco', b'sell coins')]),
            preserve_default=True,
        ),
    ]
