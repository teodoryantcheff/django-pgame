# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0012_auto_20150329_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='output',
            field=models.DecimalField(default=0, verbose_name=b'output / h', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actor',
            name='price',
            field=models.DecimalField(default=0, max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='actorprocurementhistory',
            name='price',
            field=models.DecimalField(verbose_name=b'Price of procurement', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coinconversionhistory',
            name='coins',
            field=models.DecimalField(verbose_name=b'Converted coins', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coinconversionhistory',
            name='game_currency',
            field=models.DecimalField(verbose_name=b'Received GC', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deposithistory',
            name='game_currency',
            field=models.DecimalField(verbose_name=b'Received GC', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deposithistory',
            name='real_currency',
            field=models.DecimalField(verbose_name=b'Real money', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 19, 43, 50, 261000, tzinfo=utc), verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='min_withdrawal_amount',
            field=models.DecimalField(default=0, verbose_name=b'minimum withdrawal amount', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='min_withdrawal_deposit_amount',
            field=models.DecimalField(default=0, verbose_name=b'minimum deposit amount to allow withdrawals', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='manualgamestats',
            name='cash_reserve',
            field=models.DecimalField(max_digits=16, decimal_places=5, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='manualgamestats',
            name='cash_total_paid',
            field=models.DecimalField(max_digits=16, decimal_places=5, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='balance_coins',
            field=models.DecimalField(default=0, max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='balance_i',
            field=models.DecimalField(default=0, verbose_name=b'Investment balance', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='balance_w',
            field=models.DecimalField(default=0, verbose_name=b'Withdrawal balance', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='withdrawalhistory',
            name='game_currency',
            field=models.DecimalField(verbose_name=b'GC spent', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='withdrawalhistory',
            name='real_currency',
            field=models.DecimalField(verbose_name=b'Real money received', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
    ]
