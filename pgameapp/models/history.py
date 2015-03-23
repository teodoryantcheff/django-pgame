__author__ = 'Jailbreaker'

from django.db import models
from django.conf import settings

from pgameapp.models import Actor


AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


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
        blank=False
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    actor = models.ForeignKey(
        to=Actor,
        null=False,
        blank=False
    )

    price = models.FloatField(
        verbose_name='Price of procurement',
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return 'ActorProcurementHistory'


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
        blank=False
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    coins = models.FloatField(
        verbose_name='Converted coins',
        null=False,
        blank=False
    )

    game_currency = models.FloatField(
        verbose_name='Received GC',
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return 'CoinConversionHistory'


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
        blank=False
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )

    real_currency = models.FloatField(
        verbose_name='Real money',
        null=False,
        blank=False
    )

    game_currency = models.FloatField(
        verbose_name='Received GC',
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return 'DepositHistory'


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
        blank=False
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    real_currency = models.FloatField(
        verbose_name='Real money received',
        null=False,
        blank=False
    )

    game_currency = models.FloatField(
        verbose_name='GC spent',
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):  # __str__ on python 3
        return 'WithdrawalHistory'