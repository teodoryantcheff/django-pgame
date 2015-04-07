# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pgameapp', '0045_auto_20150406_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameconfiguration',
            name='affiliate_deposit_percent',
            field=models.DecimalField(default=0, help_text=b'Affiliate deposit percent -- % of every payment given as bonus to the guy who bought the payer into the game', verbose_name=b'affiliate deposit percent', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='coin_collect_time',
            field=models.PositiveIntegerField(default=10, help_text=b'Interval between coin collects (minutes)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='coin_to_gc_rate',
            field=models.DecimalField(default=1, help_text=b'How many coins for 1 GC', verbose_name=b'coins to GC (game currency) rate', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='first_deposit_bonus_percent',
            field=models.DecimalField(default=0, help_text=b'Bonus percent @ first deposit', verbose_name=b'1st deposit bonus %', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_currency',
            field=models.CharField(default=b'Default game currency', help_text=b'Game currency - srebro, silver, gold, shitz ...', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='game_start_datetime',
            field=models.DateTimeField(help_text=b'Date of "official" game start', verbose_name=b'Date of "official" game start', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='investment_balance_percent_on_sale',
            field=models.PositiveSmallIntegerField(default=70, help_text=b'Percent GC to go to investment balance on coins sale', verbose_name=b'% GC to go to investment balance on coins sale'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='min_coins_to_sell',
            field=models.DecimalField(default=100, help_text=b'Minimum coin balance to allow selling for GC', verbose_name=b'Min coins to allow selling to GC', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='min_withdrawal_amount',
            field=models.DecimalField(default=0, help_text=b'Minimum withdrawal amount. Less than that cannot be withdrawn', verbose_name=b'minimum withdrawal amount', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='min_withdrawal_deposit_amount',
            field=models.DecimalField(default=0, help_text=b'Minimum deposit amount to allow withdrawals', verbose_name=b'minimum deposit amount to allow withdrawals', max_digits=16, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='w_to_i_conversion_bonus_percent',
            field=models.PositiveSmallIntegerField(default=99, help_text=b'Bonus (additional) percent on converting withdrawal to investment balance', verbose_name=b'Exchange bonus %'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userledger',
            name='serialized_data',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='crypto_address',
            field=models.CharField(help_text=b'Crypto address to send shit to', max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ref_campaign',
            field=models.CharField(default=b'', help_text=b'Source and campaign as set by the REFERRER who brings the guy into the game. Used for referral statistics generation', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ref_source',
            field=models.CharField(default=b'', help_text=b'Source and campaign as set by the REFERRER who brings the guy into the game. Used for referral statistics generation', max_length=64, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='referral_id',
            field=models.CharField(help_text=b'Personal id for the user to use when setting referral links', unique=True, max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='referrer',
            field=models.ForeignKey(related_name='referrals', to=settings.AUTH_USER_MODEL, help_text=b'Who brought this user into the game. Taken on account creation based on ref_code.', null=True),
            preserve_default=True,
        ),
    ]
