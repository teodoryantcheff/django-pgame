# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0031_auto_20150402_0222'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='referralstats',
            options={'verbose_name_plural': 'ReferralStats'},
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='affiliate_deposit_percent',
            field=models.DecimalField(default=0, verbose_name=b'affiliate deposit percent', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='coin_to_gc_rate',
            field=models.DecimalField(default=1, verbose_name=b'coins to GC (game currency) rate', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='first_deposit_bonus_percent',
            field=models.DecimalField(default=0, verbose_name=b'% on 1st deposit bonus', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='min_coins_to_sell',
            field=models.DecimalField(default=100, verbose_name=b'minimum coin balance to allow selling for GC', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
    ]
