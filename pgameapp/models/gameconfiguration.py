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
        # verbose_name='game currency name',
        help_text='Game currency - srebro, silver, gold, shitz ...',
        max_length=30,
        default='Default game currency'
    )

    """
    coin to GC (game currency) rate
    """
    coin_to_gc_rate = models.DecimalField(
        verbose_name='coins to GC (game currency) rate',
        help_text='How many coins for 1 GC',
        default=1,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Interval (minutes) between coin collects
    """
    coin_collect_time = models.PositiveIntegerField(
        # verbose_name='interval (minutes) between coin collects',
        help_text='Interval between coin collects (minutes)',
        default=10
    )

    """
    Minimum coin balance to allow selling for GC
    """
    min_coins_to_sell = models.DecimalField(
        verbose_name='Min coins to allow selling to GC',
        help_text='Minimum coin balance to allow selling for GC',
        default=100,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    % GC to go to investment balance on coins sale
    """
    investment_balance_percent_on_sale = models.PositiveSmallIntegerField(
        verbose_name='% GC to go to investment balance on coins sale',
        help_text='Percent GC to go to investment balance on coins sale',
        default=70,
    )

    """
    Bonus percent @ first deposit
    """
    first_deposit_bonus_percent = models.DecimalField(
        verbose_name='1st deposit bonus %',
        help_text='Bonus percent @ first deposit',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Minimum withdrawal amount. Less than that cannot be withdrawn
    """
    min_withdrawal_amount = models.DecimalField(
        verbose_name='minimum withdrawal amount',
        help_text='Minimum withdrawal amount. Less than that cannot be withdrawn',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Minimum deposit amount to allow withdrawals
    """
    min_withdrawal_deposit_amount = models.DecimalField(
        verbose_name='minimum deposit amount to allow withdrawals',
        help_text='Minimum deposit amount to allow withdrawals',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Affiliate deposit percent -- % of every payment given as bonus to the guy who bought the payer into the game
    """
    affiliate_deposit_percent = models.DecimalField(
        verbose_name='affiliate deposit percent',
        help_text='Affiliate deposit percent -- % of every payment given as bonus to the guy who bought the payer into the game',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES,
    )

    """
    Bonus (additional) percent on converting withdrawal to investment balance
    """
    w_to_i_conversion_bonus_percent = models.PositiveSmallIntegerField(
        verbose_name='Exchange bonus %',
        help_text='Bonus (additional) percent on converting withdrawal to investment balance',
        default=99
    )

    """
    Date of "official" game start
    """
    game_start_datetime = models.DateTimeField(
        verbose_name='Date of "official" game start',
        help_text='Date of "official" game start',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'game configuration'

    def __unicode__(self):  # __str__ on python 3
        return 'Game Configuration'
