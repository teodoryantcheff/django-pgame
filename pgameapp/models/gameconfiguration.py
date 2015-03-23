from django.db import models
import solo.models

__author__ = 'Jailbreaker'


class GameConfiguration(solo.models.SingletonModel):
    """
    Game configuration options
    """

    """
    Game currency - srebro, silver, gold, shitz ...
    """
    game_currency = models.CharField(
        max_length=30,
        verbose_name='Game currency name',
        default='Default game currency'
    )

    """
    coin to GC (game currency) rate
    """
    coin_to_gc_rate = models.FloatField(
        verbose_name='coins to GC (game currency) rate',
        default=1
    )

    """
    Interval (minutes) between coin collects
    """
    coin_collect_time = models.PositiveIntegerField(
        verbose_name='Interval (minutes) between coin collects',
        default=10
    )

    """
    Minimum coin balance to allow selling for GC
    """
    min_coins_to_sell = models.FloatField(
        verbose_name='Minimum coin balance to allow selling for GC',
        default=100
    )

    """
    % GC to go to investment balance on coins sale
    """
    investment_balance_percent_on_sale = models.PositiveSmallIntegerField(
        verbose_name='% GC to go to investment balance on coins sale',
        default=70,
    )

    """
    Bonus percent @ first deposit
    """
    first_deposit_bonus_percent = models.FloatField(
        verbose_name='% on 1st deposit bonus',
        default=0
    )

    """
    Minimum withdrawal amount. Less than that cannot be withdrawn
    """
    min_withdrawal_amount = models.FloatField(
        verbose_name='Minimum withdrawal amount',
        default=0
    )

    """
    Minimum deposit amount to allow withdrawals
    """
    min_withdrawal_deposit_amount = models.FloatField(
        verbose_name='Minimum deposit amount to allow withdrawals',
        default=0
    )

    """
    Affiliate deposit percent
    """
    affiliate_deposit_percent = models.FloatField(
        verbose_name='affiliate deposit percent',
        default=0
    )

    """
    Bonus (additional) percent on converting withdrawal to investment balance
    """
    w_to_i_conversion_bonus_percent = models.PositiveSmallIntegerField(
        verbose_name='Bonus (additional) percent on converting withdrawal to investment balance',
        default=99
    )

    def __unicode__(self):  # __str__ on python 3
        return 'Game Configuration'

    class Meta:
        verbose_name = 'Game Configuration'
