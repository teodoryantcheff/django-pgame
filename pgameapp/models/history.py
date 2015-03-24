from django.db import models

from . import AUTH_USER_MODEL
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

    price = models.FloatField(
        verbose_name='Price of procurement',
        null=False,
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

    coins = models.FloatField(
        verbose_name='Converted coins',
        null=False,
    )

    game_currency = models.FloatField(
        verbose_name='Received GC',
        null=False,
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return u'CoinConversionHistory'


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

    real_currency = models.FloatField(
        verbose_name='Real money',
        null=False,
    )

    game_currency = models.FloatField(
        verbose_name='Received GC',
        null=False,
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

    real_currency = models.FloatField(
        verbose_name='Real money received',
        null=False,
    )

    game_currency = models.FloatField(
        verbose_name='GC spent',
        null=False,
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return u'WithdrawalHistory'