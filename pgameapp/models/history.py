from django.db import models

from . import AUTH_USER_MODEL, DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS
from pgameapp.models import Actor


__author__ = 'Jailbreaker'


class ActorProcurementHistory(models.Model):
    """
    History of actor procurement
    """

    """
    FK to User
    """
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=False,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )

    actor = models.ForeignKey(
        to=Actor,
        null=False,
    )

    price = models.DecimalField(
        verbose_name='Price of procurement',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return u'ActorProcurementHistory'


class CoinConversionHistory(models.Model):
    """
    History of coin conversions
    """

    """
    FK to User
    """
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=False,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )

    coins = models.DecimalField(
        verbose_name='Converted coins',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    game_currency = models.DecimalField(
        verbose_name='Received GC',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return u'CoinConversionHistory'


# TODO make this to be a ledger ?
class DepositHistory(models.Model):
    """
    Deposits history
    """

    """
    FK to User
    """
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=False,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )

    real_currency = models.DecimalField(
        verbose_name='Real money',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    game_currency = models.DecimalField(
        verbose_name='Received GC',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return u'DepositHistory'


class WithdrawalHistory(models.Model):
    """
    Withdrawals history
    """

    """
    FK to User
    """
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=False,
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    real_currency = models.DecimalField(
        verbose_name='Real money received',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    game_currency = models.DecimalField(
        verbose_name='GC spent',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return u'WithdrawalHistory'