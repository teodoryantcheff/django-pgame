from django.db import models
from . import DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS, AbstractBaseHistory

__author__ = 'Jailbreaker'


class BlockProcessingHistory(AbstractBaseHistory):
    """
    History of block processing
    """

    """
    blockhash
    """
    blockhash = models.CharField(
        max_length=128,
        blank=False
    )

    """
    blockheight for the block with hash blockhash
    """
    blockheight = models.BigIntegerField(
        default=0
    )

    class Meta:
        verbose_name_plural = 'BlockProcessingHistory'
        get_latest_by = 'timestamp'

    def __unicode__(self):  # __str__ on python 3
        return u'BlockProcessingHistory at {}'.format(self.blockheight)


class TransactionsSentManager(models.Manager):
    def get_queryset(self):
        return super(TransactionsSentManager, self).get_queryset().filter(tx_type='S')


class TransactionsReceivedManager(models.Manager):
    def get_queryset(self):
        return super(TransactionsReceivedManager, self).get_queryset().filter(tx_type='R')


class CryptoTransaction(AbstractBaseHistory):
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
    crypto cash transferred
    """
    amount = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Source or destination address of the transaction
    """
    address = models.CharField(
        max_length=48
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

    def __unicode__(self):  # __str__ on python 3
        return u'{timestamp} {type} {amount:.2}'.format(
            timestamp=self.timestamp,
            type=self.tx_type,
            amount=self.amount,
        )