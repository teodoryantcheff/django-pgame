# coding=utf-8
try:
    import simplejson as json
except ImportError:
    import json

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from . import AbstractBaseUserHistory
from . import DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS


__author__ = 'Jailbreaker'


class UserLedgerManager(models.Manager):

    def log(self, user, typ, amount, object1=None, object2=None, object3=None, data=None):
        """
        Creates new log entry
        @param user             Profile
        @param affected_object  any model
        @param key              string (LogAction.name)
        """
        entry = self.model(
            user=user,
            type=typ,
            amount=amount,
        )

        if object1 is not None:
            entry.object1 = object1

        if object2 is not None:
            entry.object2 = object2

        if object3 is not None:
            entry.object3 = object3

        if data:
            entry.data = data

        entry.save(force_insert=True)
        return entry


class UserLedger(AbstractBaseUserHistory):
    # TODO proper naming
    PAYMENT = 'pmt'
    BONUS_REFERRAL_PAYMENT = 'b_rp'
    BONUS_FIRST_PAYMENT = 'b_fp'
    WITHDRAWAL = 'wdr'
    BUY_ACTOR = 'bac'
    W2I_EXCHANGE = 'w2i'
    SELL_COINS = 'sco'

    _TYPE_CHOICES = (
        (PAYMENT, 'payment'),
        (BONUS_REFERRAL_PAYMENT, 'referral bonus'),
        (BONUS_FIRST_PAYMENT, '1st payment bonus'),

        (WITHDRAWAL, 'withdrawal'),
        (BUY_ACTOR, 'buy actor'),
        (W2I_EXCHANGE, 'w2i'),
        (SELL_COINS, 'sell coins'),
    )

    amount = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Type. Types defined in _TYPE_CHOICES
    """
    type = models.CharField(
        max_length=10,
        choices=_TYPE_CHOICES,
    )

    object_type1 = models.ForeignKey(ContentType,  related_name='log_items1', null=True)
    object_id1 = models.PositiveIntegerField(null=True)
    object1 = GenericForeignKey("object_type1", "object_id1")

    object_type2 = models.ForeignKey(ContentType,  related_name='log_items2', null=True)
    object_id2 = models.PositiveIntegerField(null=True)
    object2 = GenericForeignKey("object_type2", "object_id2")

    object_type3 = models.ForeignKey(ContentType,  related_name='log_items3', null=True)
    object_id3 = models.PositiveIntegerField(null=True)
    object3 = GenericForeignKey("object_type3", "object_id3")

    serialized_data = models.TextField(null=True)

    objects = UserLedgerManager()
    _data = None

    @property
    def data(self):
        if self._data is None and self.serialized_data is not None:
            self._data = json.loads(self.serialized_data)
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.serialized_data = None

    def save(self, *args, **kwargs):
        if self._data is not None and self.serialized_data is None:
            self.serialized_data = json.dumps(self._data)
        super(UserLedger, self).save(*args, **kwargs)

    class Meta:
        ordering = ("-timestamp", )

    def __unicode__(self):
        return u'{} <{}> {} $:{}'.format(self.timestamp, self.user, self.type, self.amount)


log_leger = UserLedger.objects.log
