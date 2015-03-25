from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.db.models import Sum
from django.db.models.signals import post_save

from . import AUTH_USER_MODEL, Actor, UserActorOwnership
from django.utils.crypto import get_random_string

__author__ = 'Jailbreaker'


class UserProfile(models.Model):
    """
    User profile - Anything that is part of the user definition an is not in the PUser model comes here.
    """

    """
    FK to User
    """
    user = models.OneToOneField(
        to=AUTH_USER_MODEL,
        related_name='profile',
        primary_key=True,
        null=False,
        blank=False
    )

    """
    Personal user crypto address -- user send to this
    """
    crypto_address = models.CharField(
        # verbose_name='DOGE, bitcoin... address',
        max_length=50,
        blank=True
    )

    # """
    # User supplied cryto address -- system send to user at this
    # """
    # withdrawal_address = models.CharField(
    #     max_length=50,
    #     blank=True
    # )

    pin = models.CharField(
        verbose_name='Personal PIN',
        max_length=10,
        blank=True
    )

    balance_i = models.FloatField(verbose_name='Investment balance', default=0)
    balance_w = models.FloatField(verbose_name='Withdrawal balance', default=0)

    balance_coins = models.FloatField(default=0)

    """
    Who brought this user into the game
    """
    referrer = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='referrals',
    )

    """
    id to use for referral links. generated by the game
    """
    referral_id = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False
    )

    """
    Last time coins were collected
    """
    last_coin_collection_time = models.DateTimeField(
        auto_now_add=True,
    )

    def set_referral_info(self, ref_code, rec_cource=None, ref_campaign=None):
        """
        Sets referral info. Does NOT save() after. Call save() yourself.

        :param ref_code: Referral code
        :param rec_cource: Referral source
        :param ref_campaign: Referral campaign
        :return:
        """
        user_model = get_user_model()
        if ref_code:
            try:
                self.referrer = user_model.objects.get(profile__referral_id=ref_code)
            except user_model.DoesNotExist:
                print 'Account with referral_id {} does not exist. Ignosring'.format(ref_code)
                pass

    def set_crypto_address(self, crypto_adderess):
        self.crypto_address = crypto_adderess

    def get_total_actors(self):
        return self.user.useractorownership_set.aggregate(Sum('num_actors')).values()[0]

    class Meta:
        verbose_name = 'UserProfile'

    def __unicode__(self):  # __str__ on python 3
        return self.user.get_username()
        # return 'UserProfile'


def create_userprofile(sender, instance, created, **kwargs):
    if created:
        up, created = UserProfile.objects.get_or_create(user=instance)
        up.pin = get_random_string(6)

        while True:
            # generate referral_id
            up.referral_id = get_random_string(length=12)
            try:
                up.save()
                break  # generated referral_id is unique and user profile got saved
            except IntegrityError:
                continue  # referral_id is not unique, try again

post_save.connect(create_userprofile, sender=AUTH_USER_MODEL, dispatch_uid='post_save__User__create_userprofile')