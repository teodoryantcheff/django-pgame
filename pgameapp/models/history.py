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
        get_latest_by = 'timestamp'

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
        get_latest_by = 'timestamp'

    def __unicode__(self):  # __str__ on python 3
        return u'CoinConversionHistory'


class TransactionsSentManager(models.Manager):
    def get_queryset(self):
        return super(TransactionsSentManager, self).get_queryset().filter(tx_type='S')


class TransactionsReceivedManager(models.Manager):
    def get_queryset(self):
        return super(TransactionsReceivedManager, self).get_queryset().filter(tx_type='R')


class CryptoTransaction(models.Model):
    """
    Transactions history to and from a crypto currency -- bitcoin, litecoin, doge, etc, etc
    """
    SEND = "S"
    RECEIVE = "R"
    MOVE = "M"
    ORPHAN = "O"
    IMMATURE = "I"
    GENERATE = "G"
    TX_TYPE_CHOICES = (
        (SEND, "send"),
        (RECEIVE, "receive"),
        (MOVE, "move"),
        (ORPHAN, "orphan"),
        (IMMATURE, "immature"),
        (GENERATE, "generate"),
    )

    """
    FK to User txn got mapped to
    """
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=False,
    )

    """
    """
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    """
    crypto sent or received
    """
    crypto_currency = models.DecimalField(
        verbose_name='Real money',
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    GC received or sent
    """
    game_currency = models.DecimalField(
        null=False,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Transaction ID
    """
    txid = models.CharField(
        max_length=128
    )

    """
    Type (category) of this transaction. Types defined in TX_TYPE_CHOICES
    """
    tx_type = models.CharField(
        max_length=1,
        choices=TX_TYPE_CHOICES,
    )

    objects = models.Manager()
    sent = TransactionsSentManager()
    received = TransactionsReceivedManager()

    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'

    def __unicode__(self):  # __str__ on python 3
        return u'TX {type} {amount:.2} {user}'.format(
            type=self.tx_type,
            amount=self.crypto_currency,
            user=self.user
        )