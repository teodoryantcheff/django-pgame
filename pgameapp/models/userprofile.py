from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string

from . import AUTH_USER_MODEL, DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS


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
        # TODO unique = True
    )

    """
    User's nickname
    """
    nickname = models.CharField(
        max_length=20,
        blank=True
    )

    """
    Personal user crypto address -- user send to this
    """
    crypto_address = models.CharField(
        # verbose_name='DOGE, bitcoin... address',
        max_length=50,
        blank=True
    )

    pin = models.CharField(
        verbose_name='Personal PIN',
        max_length=10,
        blank=True
    )

    balance_i = models.DecimalField(
        verbose_name='Investment balance',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    balance_w = models.DecimalField(
        verbose_name='Withdrawal balance',
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    balance_coins = models.DecimalField(
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    Signup IP
    """
    signup_ip = models.IPAddressField(
        default='',
        blank=True,
    )

    """
    Who brought this user into the game. Taken on account creation based on ref_code and put here as a FK to a User
    """
    referrer = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=True,
        related_name='referrals',
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

    """
    id to use for referral links. generated by the game
    """
    referral_id = models.CharField(
        max_length=30,
        unique=True,
        blank=False
    )

    """
    Last time coins were collected
    """
    last_coin_collection_time = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'UserProfile'

    def __unicode__(self):  # __str__ on python 3
        return self.user.get_username()


def create_userprofile(sender, instance, created, **kwargs):
    if created:
        up, created = UserProfile.objects.get_or_create(user=instance)

        up.pin = get_random_string(6)
        # generate referral_id
        while True:
            up.referral_id = get_random_string(length=12)  # TODO make length an option
            try:
                up.save()
                break  # generated referral_id is unique and user profile got saved
            except IntegrityError:
                continue  # referral_id is not unique, try again

post_save.connect(
    create_userprofile,
    sender=AUTH_USER_MODEL,
    dispatch_uid='post_save__User__create_userprofile'
)