from django.db import models
from django.utils import timezone
import solo.models

from . import DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS

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
        verbose_name='game currency name',
        default='Default game currency'
    )

    """
    coin to GC (game currency) rate
    """
    coin_to_gc_rate = models.FloatField(
        verbose_name='coins to GC (game currency) rate',
        default=1,
    )

    """
    Interval (minutes) between coin collects
    """
    coin_collect_time = models.PositiveIntegerField(
        verbose_name='interval (minutes) between coin collects',
        default=10
    )

    """
    Minimum coin balance to allow selling for GC
    """
    min_coins_to_sell = models.FloatField(
        verbose_name='minimum coin balance to allow selling for GC',
        default=100,
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
        default=0,
    )

    """
    Minimum withdrawal amount. Less than that cannot be withdrawn
    """
    min_withdrawal_amount = models.DecimalField(
        verbose_name='minimum withdrawal amount',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Minimum deposit amount to allow withdrawals
    """
    min_withdrawal_deposit_amount = models.DecimalField(
        verbose_name='minimum deposit amount to allow withdrawals',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
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
        verbose_name='bonus (additional) percent on converting withdrawal to investment balance',
        default=99
    )

    """
    Date of "official" game start
    """
    game_start_datetime = models.DateTimeField(
        verbose_name='Date of "official" game start',
        auto_now_add=True,
        default=timezone.now()
    )

    def __unicode__(self):  # __str__ on python 3
        return 'Game Configuration'

    class Meta:
        verbose_name = 'game configuration'
