# coding=utf-8
try:
    import simplejson as json
except ImportError:
    import json

from django.db import models

from . import AUTH_USER_MODEL, DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS

__author__ = 'Jailbreaker'


class AbstractBaseHistory(models.Model):
    """
    Abstract model class that only has a timestamp field
    """
    class Meta:
        abstract = True
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )


class AbstractBaseUserHistory(AbstractBaseHistory):
    """
    Abstract model class that extends AbstractBaseHistory and only adds a FK to user
    """
    class Meta:
        abstract = True
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'

    """
    FK to User
    """
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=False,
        # related_name="%(app_label)s_%(class)s_related"
        related_name="%(class)s_related"
    )

# r = ReferralBonusPayment.objects.values('ref_source','ref_campaign').distinct().annotate(Count('id'), Sum('amount'))
# r = ReferralBonusPayment.objects.
# values('referred_user__profile__ref_source','referred_user__profile__ref_campaign').
# distinct().
# annotate(num=Count('id'), sum=Sum('amount'))
class ReferralBonusPayment(AbstractBaseUserHistory):
    """

    Note: As per https://docs.djangoproject.com/en/1.8/ref/contrib/contenttypes/#generic-relations-and-aggregation
    aggregations are not possible with GenericFK fields hence this table. ref_source and ref_campaign are copied here
    from the user profile they come from, just for speed.
    """
    referred_user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name='payer',
        related_name='ref_payments'
    )

    amount = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES,
        verbose_name='bonus received'
    )

    """
    source and campaign as set by the REFERRER who brings the guy into the game. Used
    for referral statistics generation
    """
    ref_source = models.CharField(
        max_length=64,
        default='',
        blank=True
    )

    """
    See ref_source
    """
    ref_campaign = models.CharField(
        max_length=64,
        default='',
        blank=True
    )

    class Meta:
        pass
        # verbose_name_plural = 'ReferralBonusPayment'

    def __unicode__(self):  # __str__ on python 3
        return u'ReferralBonusPayment'
